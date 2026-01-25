import React, { useState } from 'react';
import {
    Upload, RefreshCw,
    X, Scissors, Layers, Sparkles, Terminal,
    Split, History, BookOpen, ArrowRight, Layout,
    FileCode, Check, AlertCircle, FolderOpen
} from 'lucide-react';

const Dashboard = ({
    files, activity, onUpload, onGenerate, isGenerating,
    isSplitting, chapters, setChapters, onSplit, lastUploadedFile,
    onOpenFolder
}) => {
    const [selectedItems, setSelectedItems] = useState([]);
    const [mode, setMode] = useState('split');
    const [searchQuery, setSearchQuery] = useState('');

    const toggleItem = (path) => {
        setSelectedItems(prev =>
            prev.includes(path) ? prev.filter(p => p !== path) : [...prev, path]
        );
    };

    const handleSelectAll = () => {
        const allVisiblePaths = matrixItems.map(item => item.path || item.filename);
        const allSelected = allVisiblePaths.every(path => selectedItems.includes(path));

        if (allSelected && matrixItems.length > 0) {
            setSelectedItems(prev => prev.filter(path => !allVisiblePaths.includes(path)));
        } else {
            setSelectedItems(prev => {
                const newPaths = allVisiblePaths.filter(path => !prev.includes(path));
                return [...prev, ...newPaths];
            });
        }
    };

    const matrixItems = (() => {
        const items = chapters.length > 0 ? chapters.map(c => ({
            id: c.id,
            title: c.title,
            path: c.path.replace(/^transcripts[\\/]/, ''),
            filename: c.filename
        })) : files.map((f, idx) => ({
            id: idx + 1,
            title: f.name,
            path: f.path,
            filename: f.name
        }));

        return items.filter(item =>
            item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.path.toLowerCase().includes(searchQuery.toLowerCase())
        );
    })();

    const handleSourceAction = () => {
        if (mode === 'split' && lastUploadedFile) {
            onSplit(lastUploadedFile.name);
        } else {
            setChapters([]);
        }
    };

    return (
        <div className="flex-1 flex flex-col overflow-hidden bg-doc-bg text-doc-text font-sans">
            <div className="flex-1 overflow-hidden">
                <div className="grid h-full grid-cols-1 xl:grid-cols-[minmax(0,1fr)_320px] gap-4 p-4">
                    <div className="order-1 flex flex-col gap-4 overflow-hidden min-w-0 min-h-0">
                        <div className="border border-doc-border/60 rounded-xl bg-doc-sidebar/60 p-4 space-y-4 shrink-0 shadow-sm panel-glow animate-rise">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-[10px] font-bold text-doc-text-dim uppercase tracking-[0.2em]">
                                    <BookOpen className="w-3.5 h-3.5 text-doc-accent" /> Source Intake
                                </div>
                                <div className="flex bg-black/40 border border-doc-border/70 rounded-md p-0.5">
                                    <button
                                        onClick={() => setMode('split')}
                                        className={`px-4 py-1.5 rounded-md text-[10px] font-bold uppercase transition-all ${mode === 'split' ? 'bg-doc-accent text-black/90 shadow-md' : 'text-doc-text-dim hover:text-doc-text'}`}
                                    >
                                        Segment
                                    </button>
                                    <button
                                        onClick={() => setMode('single')}
                                        className={`px-4 py-1.5 rounded-md text-[10px] font-bold uppercase transition-all ${mode === 'single' ? 'bg-doc-accent text-black/90 shadow-md' : 'text-doc-text-dim hover:text-doc-text'}`}
                                    >
                                        Direct
                                    </button>
                                </div>
                            </div>

                            <div className="flex flex-col gap-3 md:flex-row md:items-stretch">
                                <label className="flex-1 min-h-[56px] flex items-center justify-center border-2 border-dashed border-doc-border/70 rounded-lg hover:border-doc-accent/50 hover:bg-black/10 cursor-pointer group transition-all">
                                    <Upload className="w-4 h-4 mr-2 text-doc-text-dim transition-colors group-hover:text-doc-accent" />
                                    <span className="text-xs text-doc-text-dim group-hover:text-doc-text font-bold">UPLOAD MARKDOWN</span>
                                    <input
                                        type="file"
                                        accept=".md"
                                        className="hidden"
                                        onChange={onUpload}
                                        multiple={mode === 'single'}
                                    />
                                </label>

                                {mode === 'split' && lastUploadedFile && (
                                    <div className="flex items-center gap-3 px-4 border border-doc-border/70 bg-black/30 rounded-lg">
                                        <FileCode className="w-4 h-4 text-doc-accent" />
                                        <span className="text-xs font-bold truncate max-w-[200px] text-white/90">{lastUploadedFile.name}</span>
                                        <button
                                            onClick={handleSourceAction}
                                            className="flex items-center gap-2 px-3 py-1.5 bg-doc-accent text-black/90 rounded-md text-[10px] font-bold hover:brightness-110 active:scale-95 transition-all shadow-lg"
                                            title={mode === 'split' ? 'Generate chapter segments' : 'Load content'}
                                        >
                                            {mode === 'split' ? <Scissors className="w-3.5 h-3.5" /> : <Layers className="w-3.5 h-3.5" />}
                                            {mode === 'split' ? 'SEGMENT' : 'LOAD'}
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="flex-1 border border-doc-border/60 rounded-xl flex flex-col overflow-hidden bg-doc-sidebar/60 shadow-sm panel-glow animate-rise min-h-0">
                            <div className="h-12 px-4 border-b border-doc-border/70 flex items-center justify-between bg-black/20 shrink-0">
                                <div className="flex items-center gap-2 text-[10px] font-bold uppercase text-doc-text-dim tracking-[0.2em]">
                                    <Split className="w-3.5 h-3.5 text-doc-accent/60" />
                                    <span>{chapters.length > 0 ? 'Segment Queue' : 'Source Queue'}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <input
                                        type="text"
                                        placeholder="Filter..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="bg-black/30 border border-doc-border/70 rounded-md px-3 py-1.5 text-[11px] w-36 outline-none focus:border-doc-accent/50 transition-all placeholder:text-doc-text-dim/40"
                                    />
                                    <button
                                        onClick={handleSelectAll}
                                        className="px-3 py-1.5 border border-doc-border/70 rounded-md text-[10px] font-bold text-doc-accent hover:border-doc-accent hover:bg-doc-accent/10 transition-all"
                                    >
                                        {(() => {
                                            const allVisiblePaths = matrixItems.map(item => item.path || item.filename);
                                            const allSelected = allVisiblePaths.every(path => selectedItems.includes(path));
                                            return allSelected && matrixItems.length > 0 ? 'DESELECT ALL' : 'SELECT ALL';
                                        })()}
                                    </button>
                                    {selectedItems.length > 0 && (
                                        <button
                                            onClick={() => setSelectedItems([])}
                                            className="flex items-center gap-1.5 px-3 py-1.5 border border-doc-border/70 rounded-md text-[10px] font-bold text-doc-text-dim hover:border-doc-accent hover:text-doc-accent transition-all"
                                        >
                                            <X className="w-3 h-3" />
                                            CLEAR ({selectedItems.length})
                                        </button>
                                    )}
                                    {(chapters.length > 0 || files.length > 0) && (
                                        <button
                                            onClick={() => {
                                                const type = chapters.length > 0 ? 'transcripts' : 'generated';
                                                onOpenFolder(type);
                                            }}
                                            className="flex items-center gap-1.5 px-3 py-1.5 border border-doc-border/70 rounded-md text-[10px] font-bold text-doc-text-dim hover:border-doc-accent hover:text-doc-accent transition-all"
                                            title="Open output folder"
                                        >
                                            <FolderOpen className="w-3.5 h-3.5" />
                                            FOLDER
                                        </button>
                                    )}
                                    {chapters.length > 0 && (
                                        <button onClick={() => setChapters([])} className="p-1.5 border border-doc-border/70 rounded-md hover:text-red-400 hover:border-red-400/50 transition-all" title="Clear chapters">
                                            <X className="w-3.5 h-3.5" />
                                        </button>
                                    )}
                                </div>
                            </div>

                            <div className="flex-1 overflow-y-auto overscroll-contain p-4 space-y-2 custom-scrollbar bg-black/10">
                                {!isSplitting && matrixItems.length === 0 && (
                                    <div className="h-full flex flex-col items-center justify-center opacity-10">
                                        <Layout className="w-12 h-12 mb-3" />
                                        <span className="text-[11px] font-bold uppercase tracking-widest">Workspace Empty</span>
                                    </div>
                                )}
                                {isSplitting && (
                                    <div className="h-full flex flex-col items-center justify-center gap-4 text-doc-accent animate-pulse">
                                        <RefreshCw className="w-8 h-8 animate-spin" />
                                        <span className="text-[10px] font-bold uppercase tracking-[0.2em]">Processing Stream...</span>
                                    </div>
                                )}
                                {!isSplitting && matrixItems.map((item, idx) => (
                                    <div
                                        key={item.path || item.filename}
                                        onClick={() => toggleItem(item.path || item.filename)}
                                        className={`flex items-center gap-4 p-3 rounded-lg border transition-all cursor-pointer group ${selectedItems.includes(item.path || item.filename) ? 'bg-doc-accent/10 border-doc-accent/40 shadow-md' : 'bg-black/30 border-doc-border/60 hover:border-doc-border hover:bg-black/40'}`}
                                    >
                                        <div className={`w-5 h-5 rounded flex items-center justify-center transition-all ${selectedItems.includes(item.path || item.filename) ? 'bg-doc-accent text-black/90' : 'bg-black border border-doc-border text-doc-text-dim group-hover:border-doc-accent/40'}`}>
                                            {selectedItems.includes(item.path || item.filename) ? <Check className="w-3.5 h-3.5" /> : <span className="text-[8px] font-bold">{idx + 1}</span>}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className={`text-[12px] font-bold truncate transition-colors ${selectedItems.includes(item.path || item.filename) ? 'text-white' : 'text-white/70 group-hover:text-white'}`}>
                                                {item.title}
                                            </div>
                                            <div className="text-[9px] text-doc-text-dim truncate mt-0.5 opacity-60 font-mono tracking-tight">
                                                {item.path}
                                            </div>
                                        </div>
                                        {item.path.endsWith('.docs.md') && (
                                            <div className="shrink-0 px-2 py-0.5 bg-green-500/10 border border-green-500/20 rounded text-[8px] font-bold text-green-500">PROCESSED</div>
                                        )}
                                    </div>
                                ))}
                            </div>

                            <div className="p-4 border-t border-doc-border/70 bg-black/20 shrink-0">
                                <button
                                    disabled={selectedItems.length === 0 || isGenerating}
                                    onClick={() => onGenerate(selectedItems, false)}
                                    className="w-full relative py-3.5 bg-doc-accent hover:brightness-110 disabled:bg-doc-border/50 disabled:text-doc-text-dim text-black/90 rounded-lg flex items-center justify-center gap-3 transition-all active:scale-[0.99] shadow-xl shadow-doc-accent/10 font-bold group"
                                >
                                    {isGenerating ? (
                                        <RefreshCw className="w-4 h-4 animate-spin" />
                                    ) : (
                                        <Sparkles className="w-4 h-4 transition-transform group-hover:rotate-12" />
                                    )}
                                    <span className="tracking-[0.1em] uppercase text-xs">
                                        {isGenerating ? 'PROCESSING SCHEMA...' : `GENERATE DOCS (${selectedItems.length})`}
                                    </span>
                                    {!isGenerating && <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />}
                                </button>
                            </div>
                        </div>
                    </div>

                    <div className="order-3 flex flex-col gap-4 overflow-hidden">
                        <div className="flex-1 border border-doc-border/60 rounded-xl flex flex-col overflow-hidden bg-doc-sidebar/60 shadow-sm panel-glow animate-rise">
                            <div className="h-12 px-4 border-b border-doc-border/70 flex items-center justify-between bg-black/20 shrink-0">
                                <div className="flex items-center gap-2 text-[10px] font-bold uppercase text-doc-text-dim tracking-[0.2em]">
                                    <History className="w-3.5 h-3.5 text-doc-accent/60" /> Run Log
                                </div>
                                <div className="flex items-center gap-1.5 px-2 py-0.5 bg-green-500/10 rounded-full border border-green-500/20">
                                    <div className="w-1 h-1 rounded-full bg-green-500 animate-pulse" />
                                    <span className="text-[8px] font-bold text-green-500 uppercase tracking-tighter">Live</span>
                                </div>
                            </div>

                            <div className="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar font-mono text-[10px] bg-black/10">
                                {activity.length === 0 && (
                                    <div className="h-full flex flex-col items-center justify-center opacity-10 gap-3">
                                        <Terminal className="w-10 h-10" />
                                        <span className="text-[9px] font-bold uppercase">Standby</span>
                                    </div>
                                )}
                                {activity.map((log, idx) => (
                                    <div
                                        key={idx}
                                        className={`p-3 border rounded-md transition-all ${log.success ? 'border-doc-accent/20 bg-doc-accent/10' : 'border-red-500/20 bg-red-500/10'}`}
                                    >
                                        <div className="flex justify-between items-center mb-1.5 opacity-40 text-[8px] font-bold">
                                            <div className="flex items-center gap-1.5">
                                                {log.success ? <Check className="w-2.5 h-2.5" /> : <AlertCircle className="w-2.5 h-2.5 text-red-400" />}
                                                <span>{new Date(log.timestamp ?? 0).toLocaleTimeString([], { hour12: false })}</span>
                                            </div>
                                            <span>{log.success ? 'COMPLETED' : 'FAILED'}</span>
                                        </div>
                                        <div className={`leading-relaxed text-[11px] font-semibold break-words ${log.success ? 'text-white/80' : 'text-red-400/90'}`}>
                                            {log.message}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="p-4 border-t border-doc-border/70 bg-black/20 space-y-3 shrink-0">
                                <div className="flex justify-between text-[9px] font-bold text-doc-text-dim">
                                    <span className="uppercase tracking-widest">System Pulse</span>
                                    <span className="text-doc-accent">STABLE</span>
                                </div>
                                <div className="h-1 bg-doc-border rounded-full overflow-hidden">
                                    <div className="h-full bg-doc-accent w-2/3 shadow-[0_0_8px_rgba(56,200,155,0.5)]" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
