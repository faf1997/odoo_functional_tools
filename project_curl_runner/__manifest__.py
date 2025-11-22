{
    "name": "Project Request Runner",
    "summary": "Store and execute curl commands linked to project tasks and server actions.",
    "version": "17.0.1.0.0",
    "author": "Francisco Fiorentino",
    "category": "Project",
    "license": "LGPL-3",
    "depends": [
        "base",
        "project",
        "project_template",
    ],
    "external_dependencies": {
        "python": ["requests", "uncurl"]
    },
    "data": [
        "security/ir.model.access.csv",
        "wizard/window_deploy_project_wizard.xml",
        "views/curl_task_views.xml",
        "views/project_task_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
    "application": True,
}
