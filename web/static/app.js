/**
 * Docalypt Web Application
 * Frontend JavaScript for the transcript-to-documentation workflow
 */

// ============================================================================
// Configuration & State
// ============================================================================

const API_BASE = '/api';

const state = {
    sessionId: null,
    uploadedFile: null,
    chapters: [],
    selectedChapters: new Set(),
    documentation: [],
    settings: {
        provider: 'ollama',
        model: '',
        temperature: 0.2,
        maxTokens: 800,
        topP: 0.9,
        topK: 40,
        endpoint: 'http://localhost:11434',
        openaiKey: '',
        anthropicKey: '',
        systemPrompt: '',
        promptTemplate: ''
    },
    currentStep: 1
};

// ============================================================================
// DOM Elements
// ============================================================================

const elements = {
    // Upload
    uploadZone: document.getElementById('upload-zone'),
    fileInput: document.getElementById('file-input'),
    fileInfo: document.getElementById('file-info'),
    fileName: document.getElementById('file-name'),
    fileSize: document.getElementById('file-size'),
    removeFile: document.getElementById('remove-file'),
    splitBtn: document.getElementById('split-btn'),
    useSingleBtn: document.getElementById('use-single-btn'),

    // Chapters
    chaptersEmpty: document.getElementById('chapters-empty'),
    chaptersList: document.getElementById('chapters-list'),
    chapterCount: document.getElementById('chapter-count'),
    selectAllChapters: document.getElementById('select-all-chapters'),
    generateBtn: document.getElementById('generate-btn'),

    // LLM Settings
    llmProvider: document.getElementById('llm-provider'),
    llmModel: document.getElementById('llm-model'),
    refreshModels: document.getElementById('refresh-models'),
    toggleAdvanced: document.getElementById('toggle-advanced'),
    advancedArrow: document.getElementById('advanced-arrow'),
    advancedSettings: document.getElementById('advanced-settings'),
    llmTemperature: document.getElementById('llm-temperature'),
    llmMaxTokens: document.getElementById('llm-max-tokens'),
    llmTopP: document.getElementById('llm-top-p'),
    llmTopK: document.getElementById('llm-top-k'),
    llmSystemPrompt: document.getElementById('llm-system-prompt'),
    llmPromptTemplate: document.getElementById('llm-prompt-template'),

    // Output
    outputEmpty: document.getElementById('output-empty'),
    outputList: document.getElementById('output-list'),
    progressContainer: document.getElementById('progress-container'),
    progressText: document.getElementById('progress-text'),
    progressPercent: document.getElementById('progress-percent'),
    progressBar: document.getElementById('progress-bar'),
    downloadBtn: document.getElementById('download-btn'),
    previewPanel: document.getElementById('preview-panel'),
    previewTitle: document.getElementById('preview-title'),
    previewContent: document.getElementById('preview-content'),
    closePreview: document.getElementById('close-preview'),

    // Status
    statusIndicator: document.getElementById('status-indicator'),
    statusText: document.getElementById('status-text'),

    // Settings Modal
    settingsBtn: document.getElementById('settings-btn'),
    settingsModal: document.getElementById('settings-modal'),
    closeSettings: document.getElementById('close-settings'),
    cancelSettings: document.getElementById('cancel-settings'),
    saveSettings: document.getElementById('save-settings'),
    settingsEndpoint: document.getElementById('settings-endpoint'),
    settingsOpenaiKey: document.getElementById('settings-openai-key'),
    settingsAnthropicKey: document.getElementById('settings-anthropic-key'),

    // Workflow
    workflowSteps: document.querySelectorAll('.workflow-step'),
    stepLines: document.querySelectorAll('.step-line'),

    // Toast
    toastContainer: document.getElementById('toast-container')
};

// ============================================================================
// Utility Functions
// ============================================================================

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showToast(message, type = 'info', duration = 4000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
        success: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>',
        error: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>',
        info: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>',
        warning: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>'
    };

    toast.innerHTML = `${icons[type] || icons.info}<span>${message}</span>`;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function updateWorkflowStep(step, completed = false) {
    state.currentStep = step;

    elements.workflowSteps.forEach((stepEl, idx) => {
        const stepNum = idx + 1;
        stepEl.classList.remove('active', 'completed');

        if (stepNum < step || (stepNum === step && completed)) {
            stepEl.classList.add('completed');
        } else if (stepNum === step) {
            stepEl.classList.add('active');
        }
    });

    // Update step lines
    elements.stepLines.forEach((line, idx) => {
        if (idx < step - 1) {
            line.classList.add('active');
        } else {
            line.classList.remove('active');
        }
    });
}

function renderMarkdown(text) {
    // Simple markdown rendering
    return text
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code>$1</code>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^(.+)$/gm, (match) => {
            if (match.startsWith('<')) return match;
            return `<p>${match}</p>`;
        });
}

// ============================================================================
// Session Management
// ============================================================================

async function createSession() {
    try {
        const data = await apiRequest('/sessions', { method: 'POST' });
        state.sessionId = data.session_id;
        console.log('Session created:', state.sessionId);
        return data;
    } catch (error) {
        showToast('Failed to create session', 'error');
        throw error;
    }
}

// ============================================================================
// File Upload
// ============================================================================

function setupFileUpload() {
    // Click to upload
    elements.uploadZone.addEventListener('click', () => {
        elements.fileInput.click();
    });

    // File input change
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Drag and drop
    elements.uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.add('dragover');
    });

    elements.uploadZone.addEventListener('dragleave', () => {
        elements.uploadZone.classList.remove('dragover');
    });

    elements.uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.remove('dragover');

        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    // Remove file
    elements.removeFile.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });
}

async function handleFileSelect(file) {
    if (!file.name.toLowerCase().endsWith('.md')) {
        showToast('Please upload a Markdown file (.md)', 'warning');
        return;
    }

    // Create session if not exists
    if (!state.sessionId) {
        await createSession();
    }

    state.uploadedFile = file;

    // Update UI
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatBytes(file.size);
    elements.fileInfo.classList.remove('hidden');
    elements.uploadZone.classList.add('has-file');
    elements.splitBtn.disabled = false;
    elements.useSingleBtn.disabled = false;

    // Upload file to server
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/upload?session_id=${state.sessionId}`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        showToast('File uploaded successfully', 'success');
        updateWorkflowStep(1, true);
        updateWorkflowStep(2);
    } catch (error) {
        showToast(`Upload failed: ${error.message}`, 'error');
        resetUpload();
    }
}

function resetUpload() {
    state.uploadedFile = null;
    elements.fileInput.value = '';
    elements.fileInfo.classList.add('hidden');
    elements.uploadZone.classList.remove('has-file');
    elements.splitBtn.disabled = true;
    elements.useSingleBtn.disabled = true;
}

async function useAsSingleChapter() {
    if (!state.sessionId || !state.uploadedFile) {
        showToast('Please upload a file first', 'warning');
        return;
    }

    elements.useSingleBtn.disabled = true;
    elements.useSingleBtn.innerHTML = '<span class="spinner"></span> Processing...';

    // Create a single chapter from the uploaded file
    const chapter = {
        index: 0,
        filename: state.uploadedFile.name,
        title: state.uploadedFile.name.replace('.md', '').replace(/[-_]/g, ' '),
        preview: 'Single chapter from uploaded file',
        path: state.uploadedFile.name  // Will be resolved server-side
    };

    // Use the split API with simple_mode which will treat as single if no headings
    try {
        const data = await apiRequest('/split', {
            method: 'POST',
            body: JSON.stringify({
                session_id: state.sessionId,
                simple_mode: true,  // This handles both split-by-headers and single-file
                export_html: false
            })
        });

        state.chapters = data.chapters;
        renderChapters(data.chapters);

        const msg = data.chapter_count === 1
            ? 'Using as single chapter'
            : `Split into ${data.chapter_count} chapters`;
        showToast(msg, 'success');
        updateWorkflowStep(2, true);
        updateWorkflowStep(3);
    } catch (error) {
        showToast(`Processing failed: ${error.message}`, 'error');
    } finally {
        elements.useSingleBtn.disabled = false;
        elements.useSingleBtn.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Single
        `;
    }
}

// ============================================================================
// Split Transcript
// ============================================================================

async function splitTranscript() {
    if (!state.sessionId || !state.uploadedFile) {
        showToast('Please upload a file first', 'warning');
        return;
    }

    elements.splitBtn.disabled = true;
    elements.useSingleBtn.disabled = true;
    elements.splitBtn.innerHTML = '<span class="spinner"></span> Splitting...';

    try {
        // Try simple_mode first (splits by headings, works for any markdown)
        const data = await apiRequest('/split', {
            method: 'POST',
            body: JSON.stringify({
                session_id: state.sessionId,
                simple_mode: true,  // Split by headings
                export_html: false
            })
        });

        state.chapters = data.chapters;
        renderChapters(data.chapters);

        showToast(`Split into ${data.chapter_count} chapters`, 'success');
        updateWorkflowStep(2, true);
        updateWorkflowStep(3);
    } catch (error) {
        showToast(`Split failed: ${error.message}`, 'error');
    } finally {
        elements.splitBtn.disabled = false;
        elements.useSingleBtn.disabled = false;
        elements.splitBtn.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path>
            </svg>
            Split
        `;
    }
}


function renderChapters(chapters) {
    if (chapters.length === 0) {
        elements.chaptersEmpty.classList.remove('hidden');
        elements.chaptersList.classList.add('hidden');
        elements.generateBtn.classList.add('hidden');
        return;
    }

    elements.chaptersEmpty.classList.add('hidden');
    elements.chaptersList.classList.remove('hidden');
    elements.generateBtn.classList.remove('hidden');
    elements.chapterCount.textContent = `(${chapters.length})`;

    // Select all by default
    state.selectedChapters = new Set(chapters.map((_, i) => i));

    elements.chaptersList.innerHTML = chapters.map((chapter, idx) => `
        <div class="chapter-item selected" data-index="${idx}">
            <div class="chapter-checkbox checked"></div>
            <div class="chapter-info">
                <div class="chapter-title">${chapter.title}</div>
                <div class="chapter-preview">${chapter.filename}</div>
            </div>
        </div>
    `).join('');

    // Add click handlers
    elements.chaptersList.querySelectorAll('.chapter-item').forEach(item => {
        item.addEventListener('click', () => toggleChapterSelection(item));
    });

    updateGenerateButton();
}

function toggleChapterSelection(item) {
    const index = parseInt(item.dataset.index);
    const checkbox = item.querySelector('.chapter-checkbox');

    if (state.selectedChapters.has(index)) {
        state.selectedChapters.delete(index);
        item.classList.remove('selected');
        checkbox.classList.remove('checked');
    } else {
        state.selectedChapters.add(index);
        item.classList.add('selected');
        checkbox.classList.add('checked');
    }

    updateGenerateButton();
}

function updateGenerateButton() {
    const count = state.selectedChapters.size;
    elements.generateBtn.disabled = count === 0 || !state.settings.model;
    elements.generateBtn.innerHTML = `
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
        Generate Documentation (${count})
    `;
}

function setupChapterControls() {
    elements.selectAllChapters.addEventListener('click', () => {
        const allSelected = state.selectedChapters.size === state.chapters.length;

        if (allSelected) {
            // Deselect all
            state.selectedChapters.clear();
            elements.chaptersList.querySelectorAll('.chapter-item').forEach(item => {
                item.classList.remove('selected');
                item.querySelector('.chapter-checkbox').classList.remove('checked');
            });
            elements.selectAllChapters.textContent = 'Select All';
        } else {
            // Select all
            state.chapters.forEach((_, i) => state.selectedChapters.add(i));
            elements.chaptersList.querySelectorAll('.chapter-item').forEach(item => {
                item.classList.add('selected');
                item.querySelector('.chapter-checkbox').classList.add('checked');
            });
            elements.selectAllChapters.textContent = 'Deselect All';
        }

        updateGenerateButton();
    });
}

// ============================================================================
// LLM Configuration
// ============================================================================

async function loadModels() {
    elements.refreshModels.disabled = true;
    elements.refreshModels.innerHTML = '<span class="spinner"></span>';

    try {
        const provider = state.settings.provider;
        let params = `provider=${provider}`;

        if (provider === 'openai' && state.settings.openaiKey) {
            params += `&api_key=${encodeURIComponent(state.settings.openaiKey)}`;
        }
        if (state.settings.endpoint) {
            params += `&endpoint=${encodeURIComponent(state.settings.endpoint)}`;
        }

        const data = await apiRequest(`/models?${params}`);

        elements.llmModel.innerHTML = '<option value="">Select a model...</option>' +
            data.models.map(model => `<option value="${model}">${model}</option>`).join('');

        if (data.models.length > 0) {
            elements.llmModel.value = data.models[0];
            state.settings.model = data.models[0];
            updateGenerateButton();
        }

        showToast(`Found ${data.models.length} models`, 'success');
    } catch (error) {
        showToast(`Failed to load models: ${error.message}`, 'error');
        elements.llmModel.innerHTML = '<option value="">No models available</option>';
    } finally {
        elements.refreshModels.disabled = false;
        elements.refreshModels.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>';
    }
}

async function checkProviders() {
    try {
        const data = await apiRequest('/providers/status');

        const available = data.filter(p => p.available);

        if (available.length > 0) {
            elements.statusIndicator.className = 'w-2 h-2 rounded-full bg-green-500';
            elements.statusText.textContent = `${available.length} provider(s) available`;
        } else {
            elements.statusIndicator.className = 'w-2 h-2 rounded-full bg-red-500';
            elements.statusText.textContent = 'No providers available';
        }

        // Auto-load models for first available provider
        const ollama = data.find(p => p.provider === 'ollama' && p.available);
        if (ollama) {
            await loadModels();
        }
    } catch (error) {
        elements.statusIndicator.className = 'w-2 h-2 rounded-full bg-red-500';
        elements.statusText.textContent = 'Connection error';
    }
}

function setupLLMSettings() {
    // Provider change
    elements.llmProvider.addEventListener('change', (e) => {
        state.settings.provider = e.target.value;
        elements.llmModel.innerHTML = '<option value="">Select a model...</option>';
        state.settings.model = '';
        updateGenerateButton();
    });

    // Model change
    elements.llmModel.addEventListener('change', (e) => {
        state.settings.model = e.target.value;
        updateGenerateButton();
    });

    // Refresh models
    elements.refreshModels.addEventListener('click', loadModels);

    // Toggle advanced settings
    elements.toggleAdvanced.addEventListener('click', () => {
        const isHidden = elements.advancedSettings.classList.contains('hidden');
        elements.advancedSettings.classList.toggle('hidden');
        elements.advancedArrow.style.transform = isHidden ? 'rotate(90deg)' : '';
    });

    // Advanced settings inputs
    elements.llmTemperature.addEventListener('change', (e) => {
        state.settings.temperature = parseFloat(e.target.value);
    });
    elements.llmMaxTokens.addEventListener('change', (e) => {
        state.settings.maxTokens = parseInt(e.target.value);
    });
    elements.llmTopP.addEventListener('change', (e) => {
        state.settings.topP = parseFloat(e.target.value);
    });
    elements.llmTopK.addEventListener('change', (e) => {
        state.settings.topK = parseInt(e.target.value);
    });
    elements.llmSystemPrompt.addEventListener('change', (e) => {
        state.settings.systemPrompt = e.target.value;
    });
    elements.llmPromptTemplate.addEventListener('change', (e) => {
        state.settings.promptTemplate = e.target.value;
    });
}

// ============================================================================
// Documentation Generation
// ============================================================================

async function generateDocumentation() {
    if (!state.sessionId || state.selectedChapters.size === 0) {
        showToast('No chapters selected', 'warning');
        return;
    }

    if (!state.settings.model) {
        showToast('Please select a model', 'warning');
        return;
    }

    elements.generateBtn.disabled = true;
    elements.generateBtn.innerHTML = '<span class="spinner"></span> Generating...';

    // Show progress
    elements.progressContainer.classList.remove('hidden');
    elements.outputEmpty.classList.add('hidden');
    elements.outputList.classList.remove('hidden');
    elements.outputList.innerHTML = '';

    const indices = Array.from(state.selectedChapters).sort((a, b) => a - b);
    const total = indices.length;
    let completed = 0;

    try {
        const data = await apiRequest('/docgen', {
            method: 'POST',
            body: JSON.stringify({
                session_id: state.sessionId,
                chapter_indices: indices,
                prompt_template: state.settings.promptTemplate || null,
                settings: {
                    provider: state.settings.provider,
                    model: state.settings.model,
                    temperature: state.settings.temperature,
                    max_tokens: state.settings.maxTokens,
                    top_p: state.settings.topP,
                    top_k: state.settings.topK,
                    system_prompt_text: state.settings.systemPrompt || null,
                    system_prompt_allow_empty: false
                }
            })
        });

        // Render results
        data.generated.forEach(item => {
            addOutputItem(item.chapter, item.documentation, false);
        });

        data.failures.forEach(item => {
            addOutputItem(item.chapter, item.error, true);
        });

        // Update progress to 100%
        updateProgress(total, total);

        if (data.successful > 0) {
            showToast(`Generated ${data.successful} documents`, 'success');
            elements.downloadBtn.classList.remove('hidden');
            updateWorkflowStep(3, true);
            updateWorkflowStep(4);
        }

        if (data.failed > 0) {
            showToast(`${data.failed} document(s) failed`, 'warning');
        }

    } catch (error) {
        showToast(`Generation failed: ${error.message}`, 'error');
    } finally {
        elements.generateBtn.disabled = false;
        elements.generateBtn.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            Generate Documentation (${state.selectedChapters.size})
        `;

        setTimeout(() => {
            elements.progressContainer.classList.add('hidden');
        }, 2000);
    }
}

function updateProgress(current, total) {
    const percent = Math.round((current / total) * 100);
    elements.progressText.textContent = `Processing ${current} of ${total}`;
    elements.progressPercent.textContent = `${percent}%`;
    elements.progressBar.style.width = `${percent}%`;
}

function addOutputItem(chapter, result, isError) {
    const item = document.createElement('div');
    item.className = `output-item ${isError ? 'error' : ''}`;
    item.innerHTML = `
        <div class="output-icon ${isError ? 'error' : 'success'}">
            ${isError
            ? '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>'
            : '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>'
        }
        </div>
        <div class="chapter-info">
            <div class="chapter-title">${result}</div>
            <div class="chapter-preview">${isError ? 'Error' : 'From'}: ${chapter}</div>
        </div>
    `;

    if (!isError) {
        item.addEventListener('click', () => showPreview(result));
    }

    elements.outputList.appendChild(item);
}

async function showPreview(docName) {
    try {
        const data = await apiRequest(`/documentation/${state.sessionId}`);
        const doc = data.documentation.find(d => d.filename === docName);

        if (doc) {
            elements.previewTitle.textContent = docName;
            elements.previewContent.innerHTML = renderMarkdown(doc.content);
            elements.previewPanel.classList.remove('hidden');
        }
    } catch (error) {
        showToast('Failed to load preview', 'error');
    }
}

// ============================================================================
// Settings Modal
// ============================================================================

function setupSettingsModal() {
    elements.settingsBtn.addEventListener('click', () => {
        elements.settingsEndpoint.value = state.settings.endpoint;
        elements.settingsOpenaiKey.value = state.settings.openaiKey;
        elements.settingsAnthropicKey.value = state.settings.anthropicKey;
        elements.settingsModal.classList.remove('hidden');
    });

    elements.closeSettings.addEventListener('click', closeSettingsModal);
    elements.cancelSettings.addEventListener('click', closeSettingsModal);

    elements.settingsModal.querySelector('.modal-backdrop').addEventListener('click', closeSettingsModal);

    elements.saveSettings.addEventListener('click', () => {
        state.settings.endpoint = elements.settingsEndpoint.value;
        state.settings.openaiKey = elements.settingsOpenaiKey.value;
        state.settings.anthropicKey = elements.settingsAnthropicKey.value;

        localStorage.setItem('docalypt_settings', JSON.stringify({
            endpoint: state.settings.endpoint,
            openaiKey: state.settings.openaiKey,
            anthropicKey: state.settings.anthropicKey
        }));

        showToast('Settings saved', 'success');
        closeSettingsModal();
    });
}

function closeSettingsModal() {
    elements.settingsModal.classList.add('hidden');
}

function loadSavedSettings() {
    const saved = localStorage.getItem('docalypt_settings');
    if (saved) {
        try {
            const settings = JSON.parse(saved);
            state.settings.endpoint = settings.endpoint || state.settings.endpoint;
            state.settings.openaiKey = settings.openaiKey || '';
            state.settings.anthropicKey = settings.anthropicKey || '';
        } catch (e) {
            console.error('Failed to load saved settings:', e);
        }
    }
}

// ============================================================================
// Download
// ============================================================================

async function downloadAll() {
    if (!state.sessionId) {
        showToast('No session available', 'warning');
        return;
    }

    try {
        window.location.href = `${API_BASE}/download/${state.sessionId}`;
        showToast('Download started', 'success');
        updateWorkflowStep(4, true);
    } catch (error) {
        showToast('Download failed', 'error');
    }
}

// ============================================================================
// Initialization
// ============================================================================

async function init() {
    console.log('Docalypt Web Application starting...');

    // Load saved settings
    loadSavedSettings();

    // Setup event handlers
    setupFileUpload();
    setupChapterControls();
    setupLLMSettings();
    setupSettingsModal();

    // Split button
    elements.splitBtn.addEventListener('click', splitTranscript);

    // Use as single chapter button
    elements.useSingleBtn.addEventListener('click', useAsSingleChapter);

    // Generate button
    elements.generateBtn.addEventListener('click', generateDocumentation);

    // Download button
    elements.downloadBtn.addEventListener('click', downloadAll);

    // Close preview
    elements.closePreview.addEventListener('click', () => {
        elements.previewPanel.classList.add('hidden');
    });

    // Create initial session
    await createSession();

    // Check provider status
    await checkProviders();

    console.log('Docalypt initialized successfully');
}

// Start the application
document.addEventListener('DOMContentLoaded', init);
