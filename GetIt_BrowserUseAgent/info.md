Browser user Agent

- Goodone which can take a query, build necessary action step required to perform that task automatically (with AI). Perform multiple actions, generate the content and extract specific information required and generate teh response
- However, it can only work with public content. Has limitation on how to do so for
  - authentication - cannot handle automatic authentication if side has login password
    - moreover we need to perform actions even with Keybased sites
  - policy driven content - always complains saying this query cannot be performed as it violates site policy
  - captcha - given policy driven content, it is obvious about captcha but not tested
- Tested with Github gpt4 model, facing lot of issues because of token limit
- Linked in network grabbing failed due to infinite scroll

# To Do

- Test with Ollama llama3.2 / mistral
