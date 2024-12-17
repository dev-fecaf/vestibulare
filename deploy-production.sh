ssh victor.silva@10.254.60.31 -p 1865 "
echo COLEGIO SER && \
cd ser-vestibulare && \
git pull origin main && \
~/.local/bin/poetry install --no-interaction --no-ansi --no-root && \
echo && \
echo ANGLO && \
cd ~/anglo-vestibulare && \
git pull origin main && \
~/.local/bin/poetry install --no-interaction --no-ansi --no-root && \
echo FINALIZADO"
