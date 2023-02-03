mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"ankitxtowod@gmail.com\"\n\
[theme]
base='light'\n\
[server]\n\
headless = true\n\
enableXsrfProtection = false
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml