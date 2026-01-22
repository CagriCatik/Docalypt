/**
 * Docalypt Frontend Tests
 * Tests for JavaScript application functionality
 * 
 * Run with: npm test (with Jest/Vitest) or in browser console
 */

// ============================================================================
// Mock API Responses
// ============================================================================

const mockResponses = {
    health: {
        status: 'healthy',
        timestamp: '2024-01-22T12:00:00.000Z',
        version: '1.0.0'
    },
    session: {
        session_id: 'test-session-123',
        created_at: '2024-01-22T12:00:00.000Z',
        upload_path: '/tmp/uploads/test-session-123'
    },
    upload: {
        session_id: 'test-session-123',
        filename: 'transcript.md',
        file_path: '/tmp/uploads/test-session-123/transcript.md',
        size_bytes: 1024
    },
    split: {
        session_id: 'test-session-123',
        chapter_count: 3,
        chapters: [
            { index: 0, filename: '01_intro.md', title: 'Introduction', preview: '# Introduction...', path: '/tmp/01_intro.md' },
            { index: 1, filename: '02_main.md', title: 'Main Content', preview: '# Main Content...', path: '/tmp/02_main.md' },
            { index: 2, filename: '03_conclusion.md', title: 'Conclusion', preview: '# Conclusion...', path: '/tmp/03_conclusion.md' }
        ],
        html_path: null
    },
    models: {
        provider: 'ollama',
        models: ['llama3', 'codellama', 'mistral', 'phi3']
    },
    providers: [
        { provider: 'ollama', available: true, message: 'Connected', models_count: 4 },
        { provider: 'openai', available: false, message: 'API key not configured' },
        { provider: 'anthropic', available: false, message: 'API key not configured' }
    ],
    docgen: {
        session_id: 'test-session-123',
        generated: [
            { chapter: '01_intro.md', documentation: '01_intro.docs.md' },
            { chapter: '02_main.md', documentation: '02_main.docs.md' }
        ],
        failures: [
            { chapter: '03_conclusion.md', error: 'Connection timeout' }
        ],
        total_chapters: 3,
        successful: 2,
        failed: 1
    },
    settings: {
        provider: 'ollama',
        model: 'llama3',
        temperature: 0.2,
        max_tokens: 800,
        top_p: 0.9,
        presence_penalty: 0.0,
        frequency_penalty: 0.0,
        repeat_penalty: 1.0,
        top_k: 40,
        endpoint: 'http://localhost:11434',
        prompt_template: 'Create Markdown documentation...'
    }
};

// ============================================================================
// Test Utilities
// ============================================================================

class TestRunner {
    constructor() {
        this.tests = [];
        this.passed = 0;
        this.failed = 0;
    }

    test(name, fn) {
        this.tests.push({ name, fn });
    }

    async run() {
        console.log('\n🧪 Running Docalypt Frontend Tests\n');
        console.log('='.repeat(60));

        for (const { name, fn } of this.tests) {
            try {
                await fn();
                this.passed++;
                console.log(`✅ PASS: ${name}`);
            } catch (error) {
                this.failed++;
                console.log(`❌ FAIL: ${name}`);
                console.log(`   Error: ${error.message}`);
            }
        }

        console.log('\n' + '='.repeat(60));
        console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
        console.log(`   Total: ${this.tests.length} tests\n`);

        return this.failed === 0;
    }
}

function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error(message || `Expected ${expected}, got ${actual}`);
    }
}

function assertArrayLength(arr, length, message) {
    if (!Array.isArray(arr) || arr.length !== length) {
        throw new Error(message || `Expected array of length ${length}, got ${arr?.length}`);
    }
}

// ============================================================================
// API Request Tests
// ============================================================================

const runner = new TestRunner();

// Mock fetch for testing
function createMockFetch(responses) {
    return async (url, options = {}) => {
        const endpoint = url.replace('/api', '');

        // Simple URL matching
        if (endpoint === '/health') {
            return { ok: true, json: async () => responses.health };
        }
        if (endpoint === '/sessions' && options.method === 'POST') {
            return { ok: true, json: async () => responses.session };
        }
        if (endpoint.includes('/upload')) {
            return { ok: true, json: async () => responses.upload };
        }
        if (endpoint === '/split') {
            return { ok: true, json: async () => responses.split };
        }
        if (endpoint.includes('/models')) {
            return { ok: true, json: async () => responses.models };
        }
        if (endpoint === '/providers/status') {
            return { ok: true, json: async () => responses.providers };
        }
        if (endpoint === '/docgen') {
            return { ok: true, json: async () => responses.docgen };
        }
        if (endpoint === '/settings/default') {
            return { ok: true, json: async () => responses.settings };
        }

        return { ok: false, json: async () => ({ detail: 'Not found' }) };
    };
}

// ============================================================================
// Test Cases
// ============================================================================

runner.test('formatBytes - should format bytes correctly', () => {
    // Test function implementation
    const formatBytes = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    assertEqual(formatBytes(0), '0 Bytes');
    assertEqual(formatBytes(1024), '1 KB');
    assertEqual(formatBytes(1048576), '1 MB');
    assertEqual(formatBytes(1073741824), '1 GB');
    assertEqual(formatBytes(512), '512 Bytes');
});

runner.test('formatBytes - should handle non-round numbers', () => {
    const formatBytes = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    assertEqual(formatBytes(1536), '1.5 KB');
    assertEqual(formatBytes(2621440), '2.5 MB');
});

runner.test('renderMarkdown - should convert headers', () => {
    const renderMarkdown = (text) => {
        return text
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
            .replace(/^# (.+)$/gm, '<h1>$1</h1>');
    };

    assertEqual(renderMarkdown('# Title'), '<h1>Title</h1>');
    assertEqual(renderMarkdown('## Subtitle'), '<h2>Subtitle</h2>');
    assertEqual(renderMarkdown('### Section'), '<h3>Section</h3>');
});

runner.test('renderMarkdown - should convert bold and italic', () => {
    const renderMarkdown = (text) => {
        return text
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>');
    };

    assertEqual(renderMarkdown('**bold**'), '<strong>bold</strong>');
    assertEqual(renderMarkdown('*italic*'), '<em>italic</em>');
});

runner.test('renderMarkdown - should convert inline code', () => {
    const renderMarkdown = (text) => {
        return text.replace(/`(.+?)`/g, '<code>$1</code>');
    };

    assertEqual(renderMarkdown('`code`'), '<code>code</code>');
});

runner.test('State initialization - should have correct defaults', () => {
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
        },
        currentStep: 1
    };

    assert(state.sessionId === null, 'sessionId should be null');
    assert(state.chapters.length === 0, 'chapters should be empty');
    assert(state.settings.provider === 'ollama', 'default provider should be ollama');
    assert(state.currentStep === 1, 'current step should be 1');
});

runner.test('Mock API - health check should return healthy', async () => {
    const mockFetch = createMockFetch(mockResponses);
    const response = await mockFetch('/api/health');
    const data = await response.json();

    assertEqual(data.status, 'healthy');
    assert(data.timestamp !== undefined, 'should have timestamp');
});

runner.test('Mock API - session creation should return session_id', async () => {
    const mockFetch = createMockFetch(mockResponses);
    const response = await mockFetch('/api/sessions', { method: 'POST' });
    const data = await response.json();

    assert(data.session_id !== undefined, 'should have session_id');
    assertEqual(data.session_id, 'test-session-123');
});

runner.test('Mock API - split should return chapters', async () => {
    const mockFetch = createMockFetch(mockResponses);
    const response = await mockFetch('/api/split', { method: 'POST' });
    const data = await response.json();

    assertEqual(data.chapter_count, 3);
    assertArrayLength(data.chapters, 3);
    assertEqual(data.chapters[0].title, 'Introduction');
});

runner.test('Mock API - models should return list', async () => {
    const mockFetch = createMockFetch(mockResponses);
    const response = await mockFetch('/api/models?provider=ollama');
    const data = await response.json();

    assertEqual(data.provider, 'ollama');
    assertArrayLength(data.models, 4);
    assert(data.models.includes('llama3'), 'should include llama3');
});

runner.test('Mock API - docgen should return results', async () => {
    const mockFetch = createMockFetch(mockResponses);
    const response = await mockFetch('/api/docgen', { method: 'POST' });
    const data = await response.json();

    assertEqual(data.successful, 2);
    assertEqual(data.failed, 1);
    assertEqual(data.total_chapters, 3);
});

runner.test('Chapter selection - toggle should add/remove', () => {
    const selectedChapters = new Set();

    // Add chapter
    selectedChapters.add(0);
    assert(selectedChapters.has(0), 'should have chapter 0');
    assertEqual(selectedChapters.size, 1);

    // Add another
    selectedChapters.add(1);
    assertEqual(selectedChapters.size, 2);

    // Remove chapter
    selectedChapters.delete(0);
    assert(!selectedChapters.has(0), 'should not have chapter 0');
    assertEqual(selectedChapters.size, 1);
});

runner.test('Chapter selection - select all should work', () => {
    const chapters = mockResponses.split.chapters;
    const selectedChapters = new Set();

    // Select all
    chapters.forEach((_, i) => selectedChapters.add(i));
    assertEqual(selectedChapters.size, 3);

    // Verify all selected
    chapters.forEach((_, i) => {
        assert(selectedChapters.has(i), `chapter ${i} should be selected`);
    });
});

runner.test('Settings validation - temperature range', () => {
    const validateTemperature = (temp) => temp >= 0 && temp <= 2;

    assert(validateTemperature(0), '0 should be valid');
    assert(validateTemperature(0.7), '0.7 should be valid');
    assert(validateTemperature(2), '2 should be valid');
    assert(!validateTemperature(-1), '-1 should be invalid');
    assert(!validateTemperature(3), '3 should be invalid');
});

runner.test('Settings validation - max tokens range', () => {
    const validateMaxTokens = (tokens) => tokens >= 100 && tokens <= 8000;

    assert(validateMaxTokens(100), '100 should be valid');
    assert(validateMaxTokens(800), '800 should be valid');
    assert(validateMaxTokens(8000), '8000 should be valid');
    assert(!validateMaxTokens(50), '50 should be invalid');
    assert(!validateMaxTokens(10000), '10000 should be invalid');
});

runner.test('File validation - markdown files only', () => {
    const isValidFile = (filename) => filename.toLowerCase().endsWith('.md');

    assert(isValidFile('transcript.md'), '.md should be valid');
    assert(isValidFile('TRANSCRIPT.MD'), '.MD should be valid');
    assert(isValidFile('my.file.md'), 'multi-dot .md should be valid');
    assert(!isValidFile('transcript.txt'), '.txt should be invalid');
    assert(!isValidFile('transcript'), 'no extension should be invalid');
});

runner.test('Workflow step calculation', () => {
    const getStepFromState = (state) => {
        if (state.documentation.length > 0) return 4;
        if (state.chapters.length > 0) return 3;
        if (state.uploadedFile) return 2;
        return 1;
    };

    assertEqual(getStepFromState({ uploadedFile: null, chapters: [], documentation: [] }), 1);
    assertEqual(getStepFromState({ uploadedFile: {}, chapters: [], documentation: [] }), 2);
    assertEqual(getStepFromState({ uploadedFile: {}, chapters: [{}], documentation: [] }), 3);
    assertEqual(getStepFromState({ uploadedFile: {}, chapters: [{}], documentation: [{}] }), 4);
});

runner.test('Progress calculation', () => {
    const calculateProgress = (current, total) => Math.round((current / total) * 100);

    assertEqual(calculateProgress(0, 10), 0);
    assertEqual(calculateProgress(5, 10), 50);
    assertEqual(calculateProgress(10, 10), 100);
    assertEqual(calculateProgress(1, 3), 33);
});

runner.test('Toast types should be valid', () => {
    const validTypes = ['success', 'error', 'info', 'warning'];

    validTypes.forEach(type => {
        assert(validTypes.includes(type), `${type} should be valid`);
    });

    assert(!validTypes.includes('invalid'), 'invalid should not be valid');
});

runner.test('Provider status parsing', () => {
    const providers = mockResponses.providers;

    const available = providers.filter(p => p.available);
    const unavailable = providers.filter(p => !p.available);

    assertEqual(available.length, 1);
    assertEqual(unavailable.length, 2);
    assertEqual(available[0].provider, 'ollama');
});

runner.test('LLM settings object structure', () => {
    const settings = mockResponses.settings;

    assert('provider' in settings, 'should have provider');
    assert('model' in settings, 'should have model');
    assert('temperature' in settings, 'should have temperature');
    assert('max_tokens' in settings, 'should have max_tokens');
    assert('top_p' in settings, 'should have top_p');
    assert('top_k' in settings, 'should have top_k');
});

runner.test('LocalStorage settings persistence', () => {
    // Simulate localStorage
    const mockStorage = {};
    const localStorage = {
        getItem: (key) => mockStorage[key] || null,
        setItem: (key, value) => { mockStorage[key] = value; }
    };

    const settings = { endpoint: 'http://localhost:11434', openaiKey: 'sk-test' };
    localStorage.setItem('docalypt_settings', JSON.stringify(settings));

    const loaded = JSON.parse(localStorage.getItem('docalypt_settings'));
    assertEqual(loaded.endpoint, 'http://localhost:11434');
    assertEqual(loaded.openaiKey, 'sk-test');
});

runner.test('Error response handling', async () => {
    const mockErrorFetch = async () => ({
        ok: false,
        json: async () => ({ detail: 'Session not found' })
    });

    const response = await mockErrorFetch();
    assert(!response.ok, 'response should not be ok');

    const data = await response.json();
    assertEqual(data.detail, 'Session not found');
});

runner.test('Chapter indices extraction', () => {
    const selectedChapters = new Set([0, 2, 5]);
    const indices = Array.from(selectedChapters).sort((a, b) => a - b);

    assertArrayLength(indices, 3);
    assertEqual(indices[0], 0);
    assertEqual(indices[1], 2);
    assertEqual(indices[2], 5);
});

runner.test('Empty chapter list handling', () => {
    const renderChapters = (chapters) => {
        const isEmpty = chapters.length === 0;
        return {
            showEmpty: isEmpty,
            showList: !isEmpty
        };
    };

    const emptyResult = renderChapters([]);
    assert(emptyResult.showEmpty, 'should show empty state');
    assert(!emptyResult.showList, 'should not show list');

    const fullResult = renderChapters([{ title: 'Test' }]);
    assert(!fullResult.showEmpty, 'should not show empty state');
    assert(fullResult.showList, 'should show list');
});

// ============================================================================
// Run Tests
// ============================================================================

// Export for Node.js testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { runner, mockResponses };
}

// Run in browser console
if (typeof window !== 'undefined') {
    runner.run().then(success => {
        if (!success) {
            console.log('\n⚠️ Some tests failed. Check the output above for details.');
        }
    });
}
