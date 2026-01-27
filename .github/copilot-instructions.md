# Copilot Instructions for heuristic_learn

- Goal: tri-agent workflow generates Socratic middle-school tutoring content with fact review before returning output.
- Pipeline: WorkflowManager in backend/workflow.py optimizes prompt once, then loops content generation + review up to 3 attempts, feeding review feedback back into generation when needed.
- Agents: prompts live in backend/agents/{prompt_optimizer_agent.py,content_generator_agent.py,knowledge_reviewer_agent.py}; reviewer must emit PASS/FAIL first line plus feedback second line so parser works.
- Model calls: all agents go through BaseAgent._call_model (dashscope Generation); prefer messages with optional system prompt; expect response.output.choices[0].message.content or response.output.text.
- Settings: backend/config/settings.py loads on import and requires DASHSCOPE_API_KEY; optional OPTIMIZER_MODEL/GENERATOR_MODEL/REVIEWER_MODEL, ALLOWED_EXTENSIONS, MAX_FILE_SIZE, DEBUG from .env.
- Server entry: backend/main.py (FastAPI) registers /learn (JSON {"topic"}) and /upload (file) plus /health; CORS wide open; run via `python backend/main.py` (uvicorn reload enabled).
- Document uploads: files saved under uploads/; DocumentProcessor enforces allowed extensions (.pdf,.docx) and max 10MB, raises ValueError if invalid; text extraction via pypdf + python-docx.
- Console flow: `python backend/console_app.py` runs interactive CLI using the same WorkflowManager.
- Tests (lightweight): `python test_core_functions.py` checks imports; `python test_console_app.py` initializes WorkflowManager and processes a sample request; `python test_review.py` exercises retry reporting; backend/test_workflow.py is stale (expects mind_map field not present) so avoid relying on it.
- End-to-end menu: `python run_full_test.py` expects backend at http://localhost:8000 for /health and /learn before proceeding; option 2 triggers batch comparison.
- Batch comparison: batch_tests/batch_test_comparison.py auto-generates student questions with qwen-flash, runs both workflow and direct qwen-max, evaluates with qwen-flash, writes reports under batch_tests/test_results_*/test_report_*.json; high API cost.
- Visualization: batch_tests/visualize_results.py (if available) can be invoked via BatchTestComparison.generate_visualization after reports exist; failures are non-fatal.
- Frontend: frontend/index.html is a static client; when running backend/main.py you can open it directly in browser and point to http://localhost:8000.
- Pathing: entry scripts extend sys.path to project root; keep module locations stable or adjust path hacks if relocating files.
- Error surfacing: WorkflowManager returns dict with review_passed, review_feedback, retry_count, final_content; errors captured as result["error"].
- Localization: user-facing strings and prompts are Chinese; preserve tone and wording when changing UX copy.
- Data persistence: upload files and batch test reports are timestamped directories; no database layer.
- External deps: fastapi, uvicorn, dashscope, pydantic_settings/pydantic fallback, requests, pypdf, python-docx; ensure these stay aligned with requirements.txt/environment.yml.
- Performance/quotas: any test hitting dashscope will spend credits; prefer mocked logic for local unit tests and gate heavy scripts behind explicit user choice.
- Adding new agents: mirror BaseAgent subclass pattern (init with model_name, implement process, use _call_model); keep structured system prompts and minimal parsing logic in one place.

## Streamlit 前端规则（近期变更）
- 工作流状态栏在 streamlit_app.py 中以单行箭头流程展示三个阶段。
- “引入对话”保持原师生配色与格式，仅首轮展示。
- “详细解释”独立于引入对话，输出为用户-AI聊天样式，且保留历史对话并按时间顺序追加在下方。
- 详细解释内容必须客观、科学、准确、信息量高，避免不必要修辞，不做老师/学生角色扮演。
- 不显示“本轮跳过对话，直接生成解释”等占位文案，避免干扰用户阅读。
