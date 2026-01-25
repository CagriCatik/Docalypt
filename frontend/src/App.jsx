import React, { useEffect, useState, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

const RAW_API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const API_BASE = RAW_API_BASE.endsWith('/api')
  ? RAW_API_BASE.replace(/\/$/, '')
  : `${RAW_API_BASE.replace(/\/$/, '')}/api`;

function App() {
  const [models, setModels] = useState([]);
  const [files, setFiles] = useState([]);
  const [prompts, setPrompts] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [activity, setActivity] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSplitting, setIsSplitting] = useState(false);
  const [chapters, setChapters] = useState([]);
  const [lastUploadedFile, setLastUploadedFile] = useState(null);
  const [defaults, setDefaults] = useState({ system_prompt: '', prompt_template: '' });

  const [config, setConfig] = useState({
    provider: 'ollama',
    model: '',
    temperature: 0.2,
    top_p: 0.9,
    max_tokens: 16384,
    presence_penalty: 0,
    frequency_penalty: 0,
    repeat_penalty: 1,
    top_k: 40,
    system_prompt: `Follow the provided instructions exactly. Maintain all technical details.`,
    prompt_template: ''
  });

  const addActivity = (entry) => {
    setActivity(prev => [{ ...entry, timestamp: Date.now() }, ...prev]);
  };

  const addActivityBatch = (entries) => {
    const now = Date.now();
    const stamped = entries.map(entry => ({ ...entry, timestamp: now }));
    setActivity(prev => [...stamped, ...prev]);
  };

  const fetchConfig = async () => {
    try {
      const res = await fetch(`${API_BASE}/config`);
      if (!res.ok) return;
      const data = await res.json();
      setDefaults({
        system_prompt: data.system_prompt ?? '',
        prompt_template: data.prompt_template ?? ''
      });
      setConfig(prev => ({
        ...prev,
        provider: data.provider ?? prev.provider,
        model: data.model ?? prev.model,
        temperature: data.temperature ?? prev.temperature,
        top_p: data.top_p ?? prev.top_p,
        max_tokens: data.max_tokens ?? prev.max_tokens,
        presence_penalty: data.presence_penalty ?? prev.presence_penalty,
        frequency_penalty: data.frequency_penalty ?? prev.frequency_penalty,
        repeat_penalty: data.repeat_penalty ?? prev.repeat_penalty,
        top_k: data.top_k ?? prev.top_k,
        system_prompt: data.system_prompt ?? prev.system_prompt,
        prompt_template: data.prompt_template ?? prev.prompt_template
      }));
    } catch (err) {
      console.error("Failed to fetch config", err);
    }
  };

  const handleOpenFolder = async (type) => {
    try {
      const res = await fetch(`${API_BASE}/open-folder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type })
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok) {
        addActivity({ success: true, message: `Opened ${type} folder.` });
      } else {
        const detail = data.detail || 'Open folder failed';
        addActivity({ success: false, message: detail });
      }
    } catch (err) {
      addActivity({ success: false, message: `Open folder error: ${err.message}` });
    }
  };

  const fetchModels = useCallback(async (provider = config.provider) => {
    try {
      const res = await fetch(`${API_BASE}/models?provider=${provider}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Failed to fetch models');
      }
      if (data.models) {
        setModels(data.models);
        if (data.models.length > 0 && (!config.model || !data.models.includes(config.model))) {
          setConfig(prev => ({ ...prev, model: data.models[0] }));
        }
      }
    } catch (err) {
      console.error("Failed to fetch models", err);
    }
  }, [config.model, config.provider]);

  const fetchFiles = async () => {
    try {
      const res = await fetch(`${API_BASE}/files`);
      const data = await res.json();
      if (data.files) {
        // Filter out files from subdirectories (split chapters)
        // Only show root-level transcript files
        const rootFiles = data.files.filter(f => !f.path.includes('/'));
        setFiles(rootFiles.reverse());
      }
    } catch (err) {
      console.error("Failed to fetch files", err);
    }
  };

  const fetchPrompts = async () => {
    try {
      const res = await fetch(`${API_BASE}/prompts`);
      const data = await res.json();
      if (data.prompts) setPrompts(data.prompts);
    } catch (err) {
      console.error("Failed to fetch prompts", err);
    }
  };

  useEffect(() => {
    fetchConfig();
    fetchFiles();
    fetchPrompts();
  }, []);

  useEffect(() => {
    fetchModels(config.provider);
  }, [config.provider, fetchModels]);

  const handlePromptSelect = async (promptName) => {
    try {
      const res = await fetch(`${API_BASE}/prompts/${promptName}`);
      const data = await res.json();
      setSelectedPrompt(data);
      setConfig(prev => ({ ...prev, prompt_template: data.content }));
    } catch (err) {
      console.error("Failed to fetch prompt content", err);
    }
  };

  const handleUpload = async (e) => {
    const filesToUpload = Array.from(e.target.files || []);
    if (filesToUpload.length === 0) return;

    const activityEntries = [];
    const uploadedNames = [];

    for (const file of filesToUpload) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
        const data = await res.json().catch(() => ({}));
        if (res.ok) {
          uploadedNames.push(data.filename || file.name);
          activityEntries.push({ success: true, message: `File uploaded: ${file.name}` });
        } else {
          const detail = data.detail || 'Upload failed';
          activityEntries.push({ success: false, message: `Upload failed (${file.name}): ${detail}` });
        }
      } catch (err) {
        activityEntries.push({ success: false, message: `Upload error (${file.name}): ${err.message}` });
      }
    }

    if (uploadedNames.length > 0) {
      fetchFiles();
    }

    if (filesToUpload.length === 1 && uploadedNames.length === 1) {
      setLastUploadedFile({ name: uploadedNames[0], size: filesToUpload[0].size });
    } else {
      setLastUploadedFile(null);
    }

    addActivityBatch(activityEntries);
    e.target.value = '';
  };

  const handleSplit = async (filename) => {
    setIsSplitting(true);
    try {
      const res = await fetch(`${API_BASE}/split`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename })
      });
      const data = await res.json();
      if (res.ok) {
        setChapters(data.chapters);
        addActivity({ success: true, message: `File split into ${data.chapters.length} parts.` });
      } else {
        addActivity({ success: false, message: `Split failed: ${data.detail || 'Error'}` });
      }
    } catch (err) {
      addActivity({ success: false, message: `Split error: ${err.message}` });
    } finally {
      setIsSplitting(false);
    }
  };

  const handleGenerate = async (selectedPaths, standalone = false) => {
    setIsGenerating(true);
    try {
      const normalizedPaths = selectedPaths.map(p => p.replace(/^transcripts[/\\]/, ''));
      const response = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          req: { files: normalizedPaths, standalone: standalone },
          config: config
        })
      });

      const data = await response.json();
      if (response.ok && data.status === 'completed') {
        if (data.generated.length > 0) {
          const newEntries = data.generated.map(msg => ({ success: true, message: msg }));
          addActivityBatch(newEntries);
        }
        if (data.failed.length > 0) {
          const failEntries = data.failed.map(msg => ({ success: false, message: msg }));
          addActivityBatch(failEntries);
        }
        fetchFiles();
      } else {
        const errorMsg = data.detail ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)) : 'Generation failed';
        addActivity({ success: false, message: errorMsg });
      }
    } catch (err) {
      addActivity({ success: false, message: `Processing error: ${err.message}` });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen w-full bg-doc-bg text-doc-text font-sans">
      <div className="flex min-h-screen w-full flex-col lg:flex-row">
        <Sidebar
          config={config}
          setConfig={setConfig}
          models={models}
          prompts={prompts}
          selectedPrompt={selectedPrompt}
          onPromptSelect={handlePromptSelect}
          defaults={defaults}
        />
        <Dashboard
          files={files}
          activity={activity}
          onUpload={handleUpload}
          onGenerate={handleGenerate}
          isGenerating={isGenerating}
          isSplitting={isSplitting}
          chapters={chapters}
          setChapters={setChapters}
          onSplit={handleSplit}
          lastUploadedFile={lastUploadedFile}
          onOpenFolder={handleOpenFolder}
        />
      </div>
    </div>
  );
}

export default App;
