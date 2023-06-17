## Story

**Goal?**
Convert an extra PC I have to a multi-purpose server with low configuration.

**What Purposes?**
Currently, I'm planning of adding a file-sharing app like Google Drive but with sharing options similar to that's of Windows on local networks. (Called it XDrive)  

**Why not use ready made software?**
* Lot's of configuration, especially for self-hosted ones.
* Battery software, where there are features I won't use anyway.
* Wanted customized features with some personalized settings.

## Tools

* Python because I'm more comfortable using it in OOP.
* To ensure structure flexibility, Flask was the framework of choice over Django:
	* It's not a battery framework as Django, So no issues of having features I won't use.
	* Provides Blueprints for a flexible project structure.
	* Ability to add specific batteries to boost development.
	* (Trying to avoid) Can add 3rd party libraries.
* PDM as a package manager, for virtual environments and deployment on other machines.
* SQLite3 because it's underrated for self-hosted projects.

## Usage

The structure is built with something similar to Django where apps are saved in `server` directory just to split global and app specific files. Skeletal structure mainly consists of:

- `server/`: Directory that contains apps.
- `static_global/`: Directory to save global static files like Bootstrap, favicon, ..etc.
- `templates/`: Directory to save global templates for Jinja to extend from. (At first it only contains `base.html`)
- `config.py`: Python file that can be imported from anywhere to access global variables.
- `filters.py`: Python file that contains custom filters to add for Jinja Engine (Imported only by app models)
- `forms.py`: Python file that contains global form configuration. (At first it only contains session-based CSRF class)
- `server_start.py`: Starting point of the Flask app.

### Run server

```
$ pdm install
$ echo App still in development.
$ pdm run db_migrate
$ pdm run dev
```

### Adding a New App

1) New apps can be added by adding a directory corresponding to it in the `server` directory. ex: `server/xdrive`. It also should follow a similar structure to this:
	* `static/`: to save app specific static files.
	* `templates/`: to save app specific template files.
	* `forms.py`: to save app forms. (each form should inherit `CSRFSessionBaseForm` to apply CSRF protection)
	* `models.py`: to save app models.
	* `routes.py`: to save app routes.
	* `admin.py`: to save app admin settings in the admin panel **(Not Implemented Yet)**

2) `routes.py` should have these lines to be able to register the app in the `server_start.py` configuration.
```
<app_name> = Blueprint(
	'<app_prefix>', __name__,
	url_prefix="/<app_url>",
	static_folder='static',
	static_url_path='static/',
	template_folder="templates"
)
```

3) Register the app in `server_start.py`. (Lines should be ~#29)
   `Here to make the app accessible from Flask`
```
from XZerver.server.<app>.routes import <app_name> as <app_name>_blueprint
blueprints = [..., <app_name>_blueprint]
```

4) Scroll down to line ~#50 and add relevant configuration for app models. 
   `Here to make the app models accessible from the admin panel`
```
from XZerver.server.<app>.models import <model> as <app_name>Model
from XZerver.server.<app>.forms import <app_form> as <app_name>From
items = {..., 
	<app_name>: {
				"model": <app_name>Model, 
				"form": <app_name>From
				}
}
```

### Creating Database

I'm using SQLAlchemy a non-migrating ORM library (noticed the non-migrating late). So It's recommended to backup your production database when developing. (Planning to refactor this dependency later.)

1) Open `database.py` file and import the model you want to add to the database.
```
from XZerver.server.<app>.models import <ModelName>
```

2) Create `.env` file and define these 3 keys: `db_seed_name`, `db_seed_email`, `db_seed_password`.

3) Run `pdm run db_migrate` to build the database. You should find it in a newly created folder called `instance`.