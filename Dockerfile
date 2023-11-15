FROM condaforge/miniforge3 AS base

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN conda install --quiet --yes poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN conda install --quiet --yes pytorch

COPY . .

ENV PATH="$VIRTUAL_ENV/bin:${PATH}"

EXPOSE 8501
CMD ["streamlit", "run", "--server.enableCORS", "false", "--browser.gatherUsageStats", "false", "app/app.py"]
