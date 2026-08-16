UI_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Command Center & HITL Approval System</title>
    <!-- Google Fonts & FontAwesome Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-amber: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.15) 0%, transparent 40%);
        }

        /* Top Header */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 2rem;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--card-border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.35rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo i {
            -webkit-text-fill-color: initial;
            color: #60a5fa;
        }

        .nav-tabs {
            display: flex;
            gap: 0.5rem;
            background: rgba(30, 41, 59, 0.5);
            padding: 0.35rem;
            border-radius: 12px;
            border: 1px solid var(--card-border);
        }

        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 0.6rem 1.2rem;
            font-size: 0.9rem;
            font-weight: 500;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tab-btn.active {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: #fff;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: var(--accent-green);
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.4; }
            50% { opacity: 1; }
            100% { opacity: 0.4; }
        }

        /* Container & Tabs */
        main {
            flex: 1;
            max-width: 1280px;
            width: 100%;
            margin: 0 auto;
            padding: 2rem;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Tab 1: Chat Layout */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 180px);
            background: var(--card-bg);
            border-radius: 16px;
            border: 1px solid var(--card-border);
            backdrop-filter: blur(16px);
            overflow: hidden;
        }

        .chat-messages {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .message {
            display: flex;
            gap: 1rem;
            max-width: 85%;
        }

        .message.user {
            align-self: flex-end;
            flex-direction: row-reverse;
        }

        .avatar {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
        }

        .message.user .avatar {
            background: linear-gradient(135deg, var(--accent-purple), #d946ef);
        }

        .message.assistant .avatar {
            background: linear-gradient(135deg, var(--accent-blue), #06b6d4);
        }

        .msg-bubble {
            background: rgba(51, 65, 85, 0.6);
            padding: 1rem 1.25rem;
            border-radius: 14px;
            line-height: 1.5;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .message.user .msg-bubble {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
            border-color: rgba(99, 102, 241, 0.3);
        }

        .tool-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
            margin-bottom: 0.5rem;
        }

        .hitl-alert-card {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .hitl-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--accent-amber);
            font-weight: 600;
        }

        .chat-controls {
            padding: 1.25rem;
            background: rgba(15, 23, 42, 0.6);
            border-top: 1px solid var(--card-border);
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .suggested-prompts {
            display: flex;
            gap: 0.5rem;
            overflow-x: auto;
            padding-bottom: 0.25rem;
        }

        .chip {
            background: rgba(51, 65, 85, 0.5);
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }

        .chip:hover {
            background: rgba(59, 130, 246, 0.2);
            color: var(--text-main);
            border-color: var(--accent-blue);
        }

        .input-row {
            display: flex;
            gap: 0.75rem;
        }

        .input-row input {
            flex: 1;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 0.8rem 1.2rem;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
        }

        .input-row input:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }

        .send-btn {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border: none;
            color: white;
            padding: 0 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .send-btn:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }

        /* Tab 2: Approvals Grid */
        .grid-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
        }

        .approval-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            gap: 1rem;
            position: relative;
        }

        .risk-tag {
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .risk-HIGH { background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); border: 1px solid var(--accent-amber); }
        .risk-CRITICAL { background: rgba(239, 68, 68, 0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }

        .approval-actions {
            display: flex;
            gap: 0.75rem;
            margin-top: 0.5rem;
        }

        .btn-approve {
            flex: 1;
            background: rgba(16, 185, 129, 0.2);
            border: 1px solid var(--accent-green);
            color: var(--accent-green);
            padding: 0.6rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-approve:hover {
            background: var(--accent-green);
            color: white;
        }

        .btn-reject {
            flex: 1;
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            padding: 0.6rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-reject:hover {
            background: var(--accent-red);
            color: white;
        }

        /* Tab 3: Audit Table */
        .table-wrapper {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            backdrop-filter: blur(12px);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th, td {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--card-border);
        }

        th {
            background: rgba(15, 23, 42, 0.6);
            color: var(--text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        td {
            font-size: 0.9rem;
        }

        /* Tab 4: Evaluations Dashboard */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 1.25rem;
            backdrop-filter: blur(12px);
        }

        .stat-val {
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.4rem 0;
            background: linear-gradient(135deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .code-box {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 8px;
            padding: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            overflow-x: auto;
            color: #a5b4fc;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo">
            <i class="fa-solid fa-robot"></i>
            <span>AI Agent Command Center</span>
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('chat')"><i class="fa-solid fa-comments"></i> Chat</button>
            <button class="tab-btn" onclick="switchTab('approvals')"><i class="fa-solid fa-shield-halved"></i> Approvals (<span id="approval-count">0</span>)</button>
            <button class="tab-btn" onclick="switchTab('logs')"><i class="fa-solid fa-list-check"></i> Audit Logs</button>
            <button class="tab-btn" onclick="switchTab('evaluations')"><i class="fa-solid fa-chart-line"></i> Evaluations</button>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div>
            <span>System Live</span>
        </div>
    </header>

    <main>
        <!-- Tab 1: Chat -->
        <div id="tab-chat" class="tab-content active">
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages">
                    <div class="message assistant">
                        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                        <div class="msg-bubble">
                            Hello! I am your AI Agent assistant. I can query accounts, check system diagnostics, or execute transfers. 
                            <br><br>
                            <em>Note: Risky tool calls will pause and require human authorization before execution.</em>
                        </div>
                    </div>
                </div>
                <div class="chat-controls">
                    <div class="suggested-prompts">
                        <div class="chip" onclick="setPrompt('Search account details for user Alice')">🔍 Query Alice Account</div>
                        <div class="chip" onclick="setPrompt('What is the system status and health?')">⚡ System Health Check</div>
                        <div class="chip" onclick="setPrompt('Transfer $300 from ACC-1001 to ACC-1002')">💸 Transfer $300 (Risky HITL)</div>
                        <div class="chip" onclick="setPrompt('Suspend account ACC-1030 for security audit')">🔒 Suspend Account (Risky HITL)</div>
                    </div>
                    <div class="input-row">
                        <input type="text" id="chat-input" placeholder="Type a message or instruction..." onkeypress="handleKeyPress(event)">
                        <button class="send-btn" onclick="sendMessage()"><i class="fa-solid fa-paper-plane"></i> Send</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab 2: Approvals -->
        <div id="tab-approvals" class="tab-content">
            <h2 style="margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;">
                <i class="fa-solid fa-shield-halved" style="color: var(--accent-amber);"></i>
                Pending Human Approval Requests
            </h2>
            <div class="grid-cards" id="approvals-grid">
                <!-- Dynamic Approval Cards -->
            </div>
        </div>

        <!-- Tab 3: Logs -->
        <div id="tab-logs" class="tab-content">
            <h2 style="margin-bottom: 1.5rem;"><i class="fa-solid fa-list-check"></i> Audit Logs & Trace Stream</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Event Type</th>
                            <th>Action</th>
                            <th>Tool</th>
                            <th>Status</th>
                            <th>Latency</th>
                        </tr>
                    </thead>
                    <tbody id="logs-table-body">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Tab 4: Evaluations -->
        <div id="tab-evaluations" class="tab-content">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h2><i class="fa-solid fa-chart-line"></i> Quality & Safety Evaluations</h2>
                <button class="send-btn" onclick="runBenchmark()"><i class="fa-solid fa-play"></i> Run Benchmark Suite</button>
            </div>
            
            <div class="stats-grid" id="stats-summary">
                <div class="stat-card">
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Tool Selection Accuracy</div>
                    <div class="stat-val" id="stat-accuracy">100%</div>
                </div>
                <div class="stat-card">
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Safety (HITL Compliance)</div>
                    <div class="stat-val" id="stat-safety">100%</div>
                </div>
                <div class="stat-card">
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Faithfulness Score</div>
                    <div class="stat-val" id="stat-faithfulness">1.0 / 1.0</div>
                </div>
                <div class="stat-card">
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Total Evaluation Runs</div>
                    <div class="stat-val" id="stat-total">0</div>
                </div>
            </div>

            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Run ID</th>
                            <th>Prompt</th>
                            <th>Tool Used</th>
                            <th>Accuracy</th>
                            <th>Safety Score</th>
                            <th>Feedback</th>
                        </tr>
                    </thead>
                    <tbody id="evals-table-body">
                        <!-- Dynamic Evals -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        let currentConversationId = null;

        function switchTab(tabName) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');

            if (tabName === 'approvals') fetchApprovals();
            if (tabName === 'logs') fetchLogs();
            if (tabName === 'evaluations') fetchEvaluations();
        }

        function setPrompt(text) {
            document.getElementById('chat-input').value = text;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        async function sendMessage() {
            const input = document.getElementById('chat-input');
            const msgText = input.value.trim();
            if (!msgText) return;

            // Render User Bubble
            appendMessage('user', msgText);
            input.value = '';

            try {
                const response = await fetch('/api/v1/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msgText, conversation_id: currentConversationId })
                });

                const data = await response.json();
                currentConversationId = data.conversation_id;

                if (data.approval_required) {
                    appendHitlMessage(data);
                    fetchApprovals();
                } else {
                    let text = data.response;
                    if (data.tool_executed) {
                        text = `<div class="tool-badge"><i class="fa-solid fa-wrench"></i> Tool Executed: ${data.tool_executed}</div><br>` + text;
                    }
                    appendMessage('assistant', text);
                }
            } catch (err) {
                appendMessage('assistant', `<span style="color: var(--accent-red)">Error communicating with Agent backend.</span>`);
            }
        }

        function appendMessage(role, htmlContent) {
            const container = document.getElementById('chat-messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${role}`;
            
            const icon = role === 'user' ? 'fa-user' : 'fa-robot';
            msgDiv.innerHTML = `
                <div class="avatar"><i class="fa-solid ${icon}"></i></div>
                <div class="msg-bubble">${htmlContent}</div>
            `;
            
            container.appendChild(msgDiv);
            container.scrollTop = container.scrollHeight;
        }

        function appendHitlMessage(data) {
            const container = document.getElementById('chat-messages');
            const details = data.approval_details;
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message assistant';
            
            msgDiv.innerHTML = `
                <div class="avatar"><i class="fa-solid fa-shield-halved" style="color: var(--accent-amber)"></i></div>
                <div class="msg-bubble">
                    ${data.response}
                    <div class="hitl-alert-card">
                        <div class="hitl-header"><i class="fa-solid fa-triangle-exclamation"></i> RISKY TOOL INTERCEPTED: ${details.tool_name}</div>
                        <div class="code-box">${JSON.stringify(details.tool_args, null, 2)}</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">Risk Level: <strong>${details.risk_level}</strong> | ID: <code>${details.approval_id}</code></div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem;">
                            <button class="btn-approve" onclick="processApproval('${details.approval_id}', 'APPROVED')">✅ Approve & Execute</button>
                            <button class="btn-reject" onclick="processApproval('${details.approval_id}', 'REJECTED')">❌ Reject Action</button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(msgDiv);
            container.scrollTop = container.scrollHeight;
        }

        async function fetchApprovals() {
            try {
                const res = await fetch('/api/v1/approvals');
                const approvals = await res.json();
                document.getElementById('approval-count').innerText = approvals.length;

                const grid = document.getElementById('approvals-grid');
                if (approvals.length === 0) {
                    grid.innerHTML = `<div style="color: var(--text-muted); grid-column: 1/-1;">No pending approvals waiting for review.</div>`;
                    return;
                }

                grid.innerHTML = approvals.map(app => `
                    <div class="approval-card">
                        <div class="risk-tag risk-${app.risk_level}">${app.risk_level} RISK</div>
                        <h3 style="font-size: 1.1rem;"><i class="fa-solid fa-bolt" style="color: var(--accent-amber);"></i> ${app.tool_name}</h3>
                        <div class="code-box">${JSON.stringify(app.tool_args, null, 2)}</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">${app.justification}</div>
                        <div class="approval-actions">
                            <button class="btn-approve" onclick="processApproval('${app.id}', 'APPROVED')">Approve</button>
                            <button class="btn-reject" onclick="processApproval('${app.id}', 'REJECTED')">Reject</button>
                        </div>
                    </div>
                `).join('');
            } catch(e) {}
        }

        async function processApproval(approvalId, action) {
            try {
                const res = await fetch(`/api/v1/approvals/${approvalId}/respond`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: action, responded_by: 'admin@dashboard.com' })
                });
                const result = await res.json();

                appendMessage('assistant', `<strong>[HITL DECISION: ${action}]</strong><br>${result.message}<br><div class="code-box">${JSON.stringify(result.execution_result, null, 2)}</div>`);
                fetchApprovals();
            } catch(e) {
                alert("Failed to process approval.");
            }
        }

        async function fetchLogs() {
            try {
                const res = await fetch('/api/v1/logs');
                const logs = await res.json();
                const tbody = document.getElementById('logs-table-body');

                tbody.innerHTML = logs.map(l => `
                    <tr>
                        <td style="color: var(--text-muted); font-size: 0.8rem;">${new Date(l.created_at).toLocaleTimeString()}</td>
                        <td><span class="tool-badge">${l.event_type}</span></td>
                        <td>${l.action}</td>
                        <td><code>${l.tool_name || '-'}</code></td>
                        <td><strong style="color: ${l.status === 'SUCCESS' ? 'var(--accent-green)' : 'var(--accent-amber)'}">${l.status}</strong></td>
                        <td>${l.execution_time_ms ? l.execution_time_ms + ' ms' : '-'}</td>
                    </tr>
                `).join('');
            } catch(e) {}
        }

        async function fetchEvaluations() {
            try {
                const res = await fetch('/api/v1/evaluations');
                const data = await res.json();
                
                if (data.metrics_summary) {
                    const m = data.metrics_summary;
                    document.getElementById('stat-accuracy').innerText = Math.round(m.avg_tool_selection_accuracy * 100) + '%';
                    document.getElementById('stat-safety').innerText = Math.round(m.avg_safety_score * 100) + '%';
                    document.getElementById('stat-faithfulness').innerText = m.avg_faithfulness_score.toFixed(2) + ' / 1.0';
                    document.getElementById('stat-total').innerText = m.total_evaluations;
                }

                const tbody = document.getElementById('evals-table-body');
                tbody.innerHTML = (data.runs || []).map(r => `
                    <tr>
                        <td><code>${r.id.substring(0, 8)}</code></td>
                        <td>${r.user_prompt}</td>
                        <td><code>${r.actual_tool || '-'}</code></td>
                        <td>${Math.round(r.scores.tool_accuracy * 100)}%</td>
                        <td>${Math.round(r.scores.safety * 100)}%</td>
                        <td style="font-size: 0.85rem; color: var(--text-muted);">${r.feedback}</td>
                    </tr>
                `).join('');
            } catch(e) {}
        }

        async function runBenchmark() {
            try {
                await fetch('/api/v1/evaluations/run', { method: 'POST' });
                fetchEvaluations();
            } catch(e) {}
        }

        // Initial fetch
        fetchApprovals();
    </script>
</body>
</html>
"""
