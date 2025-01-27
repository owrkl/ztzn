#!/usr/bin/env bash

cat <<'EOF'
$$$$$$$$\ $$$$$$$$\ $$\                           
\____$$  |\__$$  __|$$ |                          
    $$  /    $$ |   $$$$$$$\   $$$$$$\  $$$$$$$\  
   $$  /     $$ |   $$  __$$\ $$  __$$\ $$  __$$\ 
  $$  /      $$ |   $$ |  $$ |$$ /  $$ |$$ |  $$ |
 $$  /       $$ |   $$ |  $$ |$$ |  $$ |$$ |  $$ |
$$$$$$$$\    $$ |   $$ |  $$ |\$$$$$$  |$$ |  $$ |
\________|   \__|   \__|  \__| \______/ \__|  \__|
                                                  
                                                  
                                                  
Copyright (C) 2020-2024 by Zelzal-SC@Github, < https://github.com/Zelzal-SC >.
This file is part of < https://github.com/Zelzal-SC/ZTZ > project,
and is released under the "GNU v3.0 License Agreement".
Please see < https://github.com/Zelzal-SC/ZTZ/blob/main/LICENSE >
All rights reserved.
EOF

python3 keep_alive.py & gunicorn app:app --daemon & python -m zlzl
