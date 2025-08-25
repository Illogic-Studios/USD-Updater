# USD Updater

## What is this ?

This tool gives an interactive way to update USD files on a Prism-based pipeline.
For a given USD, it will check if there is a new version available for each dependency
Then allow their update.

Given a specific shot USD export, it will be to retrieve a given list of layers and will also parse them.

<img width="1198" height="830" alt="image" src="https://github.com/user-attachments/assets/2b8728b8-fa39-41bb-84bd-35716321afd2" />

## Notes

There is currently 3 modes, one for Prism, one for Maya and one for Houdini.

Prism and Houdini are very similar as they start with a given USD filepath.
The only differnce is that the Houdini modes will also look for path in selected 
Prism Import LOP nodes.

While these 2 modes use standard USD API to parse depedencies ([https://openusd.org/dev/api/dependencies_8h.html](https://openusd.org/dev/api/dependencies_8h.html)).
The Maya mode is more rough as it just parsed the current work layer as an USDA and use regular expression to get dependencies.

## Where to use it

### Prism Mode :

This mode is started from Prism Project browser product windows and is added with a prism plugin [https://prism-pipeline.com/docs/latest/development/developingPlugins/](https://prism-pipeline.com/docs/latest/development/developingPlugins/)

### Houdini and Maya :

Located as custom button in both DCC shelves.
