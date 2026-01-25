import React, { useState } from 'react';
import { Settings, Cpu, Sliders, HelpCircle, Wand2, ChevronDown, Check } from 'lucide-react';

const Sidebar = ({ config, setConfig, models, prompts, selectedPrompt, onPromptSelect, defaults }) => {
    const [showPromptList, setShowPromptList] = useState(false);

    const handleChange = (key, value) => {
        setConfig(prev => ({ ...prev, [key]: value }));
    };

    const handleReset = (type) => {
        if (type === 'persona') {
            setConfig(prev => ({ ...prev, system_prompt: defaults.system_prompt }));
        } else if (type === 'template') {
            setConfig(prev => ({ ...prev, prompt_template: defaults.prompt_template }));
        }
    };

    return (
        <aside className="w-full lg:w-80 xl:w-96 border-b lg:border-b-0 lg:border-r border-doc-border/40 flex flex-col bg-doc-sidebar/80 backdrop-blur">
            <div className="px-6 py-5 border-b border-doc-border/30">
                <div className="flex items-center gap-4">
                    <img
                        src="/assets/logo.png"
                        alt="Docalypt logo"
                        className="w-12 h-12 rounded-2xl object-contain"
                    />
                    <div className="space-y-1">
                        <div className="flex items-center gap-2 text-sm font-semibold tracking-tight text-white/90">
                            <Settings className="w-4 h-4 text-doc-accent" /> AI Control Deck
                        </div>
                        <p className="text-[11px] text-doc-text-dim leading-relaxed">
                            Tune the model, parameters, and generation constraints before each run.
                        </p>
                    </div>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar px-6 py-5 space-y-5">
                {/* Model Selection */}
                <div className="rounded-2xl bg-black/30 p-4 space-y-4 shadow-[inset_0_0_0_1px_rgba(255,255,255,0.04)]">
                    <div className="flex items-center text-[9px] font-semibold text-doc-text-dim uppercase tracking-[0.24em]">
                        <Cpu className="w-3.5 h-3.5 mr-2" /> Model Selection
                    </div>
                    <div className="space-y-3">
                        <div className="flex flex-col gap-1.5">
                            <label className="text-[9px] text-doc-text-dim font-semibold tracking-[0.2em]">PROVIDER</label>
                            <select
                                value={config.provider}
                                onChange={(e) => handleChange('provider', e.target.value)}
                                className="w-full text-xs font-medium bg-black/40 border border-white/5 focus:border-doc-accent/60"
                            >
                                <option value="ollama">Ollama (Local)</option>
                                <option value="openai">OpenAI Compatible</option>
                                <option value="anthropic">Anthropic Claude</option>
                            </select>
                        </div>
                        <div className="flex flex-col gap-1.5">
                            <label className="text-[9px] text-doc-text-dim font-semibold tracking-[0.2em]">LOCAL MODEL</label>
                            <select
                                value={config.model}
                                onChange={(e) => handleChange('model', e.target.value)}
                                className="w-full text-xs font-medium bg-black/40 border border-white/5 focus:border-doc-accent/60"
                            >
                                <option value="" disabled>Select model</option>
                                {models.map(m => <option key={m} value={m}>{m}</option>)}
                            </select>
                            {config.provider !== 'ollama' && (
                                <div className="text-[9px] text-doc-text-dim mt-1">
                                    Cloud providers use server-side API keys and endpoints.
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Parameters */}
                <div className="rounded-2xl bg-black/30 p-4 space-y-4 shadow-[inset_0_0_0_1px_rgba(255,255,255,0.04)]">
                    <div className="flex items-center text-[9px] font-semibold text-doc-text-dim uppercase tracking-[0.24em]">
                        <Sliders className="w-3.5 h-3.5 mr-2" /> Generation Params
                    </div>

                    <ParamSlider
                        label="Temperature"
                        value={config.temperature} min={0} max={2} step={0.1}
                        onChange={(v) => handleChange('temperature', v)}
                        tooltip="Controls randomness: 0 is deterministic, 1 is creative, 2 is wild."
                    />

                    <ParamSlider
                        label="Top P"
                        value={config.top_p} min={0} max={1} step={0.05}
                        onChange={(v) => handleChange('top_p', v)}
                        tooltip="Nucleus sampling: filters the top tokens by cumulative probability."
                    />

                        <div className="flex flex-col gap-1.5 group">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-1.5 group/label">
                                    <label className="text-[9px] text-doc-text-dim font-semibold uppercase tracking-[0.2em]">Max Length</label>
                                    <Tooltip text="The maximum number of tokens the model can generate per request." />
                                </div>
                            </div>
                        <input
                            type="number"
                            value={config.max_tokens}
                            onChange={(e) => {
                                const value = Number.parseInt(e.target.value, 10);
                                handleChange('max_tokens', Number.isNaN(value) ? config.max_tokens : value);
                            }}
                            className="w-full font-mono text-xs bg-black/40 border border-white/5 focus:border-doc-accent/60"
                        />
                    </div>

                    <ParamSlider
                        label="Top K"
                        value={config.top_k || 40} min={1} max={100} step={1}
                        onChange={(v) => handleChange('top_k', v)}
                        tooltip="Limits the next token selection to the top K most likely tokens."
                    />

                    <ParamSlider
                        label="Novelty Pen."
                        value={config.presence_penalty} min={-2} max={2} step={0.1}
                        onChange={(v) => handleChange('presence_penalty', v)}
                        tooltip="Incentivizes the model to talk about new topics."
                    />

                    <ParamSlider
                        label="Repeat Pen."
                        value={config.repeat_penalty} min={0.5} max={2} step={0.1}
                        onChange={(v) => handleChange('repeat_penalty', v)}
                        tooltip="Discourages the model from repeating the same lines or phrases."
                    />

                    <ParamSlider
                        label="Freq. Penalty"
                        value={config.frequency_penalty || 0} min={-2} max={2} step={0.1}
                        onChange={(v) => handleChange('frequency_penalty', v)}
                        tooltip="Decreases the likelihood of repeating exact same words/phrases based on freq."
                    />
                </div>

                {/* Instruction Studio */}
                <div className="rounded-2xl bg-black/30 p-4 space-y-4 shadow-[inset_0_0_0_1px_rgba(255,255,255,0.04)]">
                    <div className="flex items-center gap-2 text-[9px] font-semibold text-doc-text-dim uppercase tracking-[0.24em]">
                        <Wand2 className="w-3.5 h-3.5" /> Instruction Studio
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center px-1">
                            <label className="text-[9px] font-semibold text-doc-text-dim uppercase tracking-[0.2em]">Template</label>
                            <button onClick={() => handleReset('template')} className="text-[10px] text-doc-accent hover:text-white transition-colors">Reset</button>
                        </div>
                        <div className="relative">
                            <button
                                onClick={() => setShowPromptList(!showPromptList)}
                                className="w-full text-left bg-black/40 border border-white/5 rounded-md px-3 py-2 text-xs flex justify-between items-center hover:bg-black/50 transition-all"
                            >
                                <span className="truncate pr-2">{selectedPrompt?.title || 'User Template'}</span>
                                <ChevronDown className={`w-3.5 h-3.5 text-doc-text-dim transition-transform ${showPromptList ? 'rotate-180' : ''}`} />
                            </button>
                            {showPromptList && (
                                <div className="absolute top-full left-0 right-0 mt-2 bg-doc-sidebar border border-doc-border rounded-md shadow-2xl z-50 max-h-60 overflow-y-auto custom-scrollbar">
                                    {(prompts || []).map(p => {
                                        const isSelected = selectedPrompt?.name === p.name;
                                        return (
                                            <div
                                                key={p.name}
                                                onClick={() => { onPromptSelect(p.name); setShowPromptList(false); }}
                                                className={`p-3 cursor-pointer border-b border-doc-border/50 last:border-0 transition-all flex items-start gap-2 ${isSelected
                                                        ? 'bg-doc-accent/15 border-l-2 border-l-doc-accent'
                                                        : 'hover:bg-doc-accent/10'
                                                    }`}
                                            >
                                                <div className="flex-1 min-w-0">
                                                    <div className={`text-[11px] font-bold ${isSelected ? 'text-doc-accent' : 'text-white/90'}`}>
                                                        {p.title}
                                                    </div>
                                                    <div className="text-[9px] text-doc-text-dim truncate mt-0.5">
                                                        {p.description}
                                                    </div>
                                                </div>
                                                {isSelected && (
                                                    <Check className="w-4 h-4 text-doc-accent shrink-0 mt-0.5" />
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center px-1">
                            <label className="text-[9px] font-semibold text-doc-text-dim uppercase tracking-[0.2em]">System Prompt</label>
                            <button onClick={() => handleReset('persona')} className="text-[10px] text-doc-accent hover:text-white transition-colors">Reset</button>
                        </div>
                        <textarea
                            className="w-full min-h-[160px] bg-black/40 border border-white/5 rounded-md p-3 text-xs leading-relaxed resize-none custom-scrollbar focus:border-doc-accent/60 outline-none transition-all placeholder:text-white/5"
                            value={config.system_prompt || ''}
                            onChange={(e) => setConfig(prev => ({ ...prev, system_prompt: e.target.value }))}
                            placeholder="Add constraints for the processing engine..."
                        />
                    </div>
                </div>
            </div>

            <div className="px-6 py-4 border-t border-doc-border/30 bg-black/20">
                <div className="flex items-center justify-between px-1">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]" />
                        <span className="text-[10px] uppercase font-bold text-doc-text-dim">Status: Ready</span>
                    </div>
                    <span className="text-[9px] text-doc-text-dim font-mono">v1.0.9</span>
                </div>
            </div>
        </aside>
    );
};

const ParamSlider = ({ label, value, min, max, step, onChange, tooltip }) => (
    <div className="space-y-2.5 group">
        <div className="flex justify-between items-center px-0.5">
            <div className="flex items-center gap-1.5 group/label">
                <span className="text-[9px] text-doc-text-dim font-semibold uppercase tracking-[0.2em]">{label}</span>
                {tooltip && <Tooltip text={tooltip} />}
            </div>
            <span className="text-doc-accent font-mono text-[10px] font-semibold tracking-tight">{value.toFixed(label.includes('K') || label.includes('Length') ? 0 : 1)}</span>
        </div>
        <input
            type="range" min={min} max={max} step={step} value={value}
            onChange={(e) => onChange(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-white/5 rounded-full appearance-none cursor-pointer accent-doc-accent"
        />
    </div>
);

const Tooltip = ({ text }) => (
    <div className="relative group/tooltip inline-block cursor-help transition-opacity opacity-50 hover:opacity-100">
        <HelpCircle className="w-3 h-3 text-doc-text-dim" />
        <div className="absolute left-6 top-1/2 -translate-y-1/2 w-48 p-2 bg-doc-sidebar border border-doc-border rounded shadow-2xl text-[10px] text-white/80 font-medium leading-tight z-[100] invisible group-hover/tooltip:visible opacity-0 group-hover/tooltip:opacity-100 transition-all">
            {text}
        </div>
    </div>
);

export default Sidebar;
