## How to set up

- Rename the `.env.sample` file to `.env` and add all listed entries <br>

- Install pipenv:<br>
  ` pip install pipenv`

- Check if pipenv is installed:<br>
  `pipenv --version` <br>
  `>> pipenv, version 2018.11.26`

- Spawn a shell in a virtual environment<br>
  ` pipenv shell`

- List all dependencies currently installed<br>
  `pipenv lock -r`

- Install dependencies in piplock file<br>
  `pipenv sync `

- Install new dependency <br>
  `pipenv install <dependency name here> `

- Regenerate lock file after new dependency installations<br>
  `pipenv lock `

- Uninstall dependency<br>
  `pipenv uninstall <dependency name here> `

- Turn off a virtual environment<br>
  `exit`
