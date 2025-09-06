# Codex_AIPM
Hands-on Codex environment and AI PM demo project: prompts, evals, and minimal LLM app.
## Quickstart
bash infra/install.sh

uvicorn src.classifier_api:app --host 0.0.0.0 --port 8000

## Snake Game Example
The `src` directory now contains a small FastAPI demo in
`classifier_api.py` and a terminal Snake game in `snake_game.py`.


### Run the game
```bash
python src/snake_game.py
```
Use the arrow keys to move the snake and press `q` to quit.

The game renders each column twice so horizontal and vertical movement
appear at the same speed.


### GitHub workflow overview
1. **Clone the repository**: `git clone <repository-url>`
2. **Check status**: `git status`
3. **Stage changes**: `git add <file>`
4. **Commit**: `git commit -m "meaningful message"`
5. **Push to GitHub**: `git push`
6. **Open a Pull Request** on GitHub to merge your work.
