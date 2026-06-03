FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

WORKDIR /app

# Install uv for fast dependency management (optional but good practice since project uses it)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv
ENV PATH="/uvbin:${PATH}"

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the files
COPY . .

# Ensure playwright browsers are installed (though they should be in the base image)
# Actually, the base image has them, but we might need to make sure they are accessible to uv's venv
RUN uv run playwright install chromium

ENTRYPOINT ["uv", "--project", "/app", "run", "python", "/app/render_excalidraw.py"]
