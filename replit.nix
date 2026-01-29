{ pkgs }:

{
  deps = [
    pkgs.python311
    pkgs.python311Packages.django
    pkgs.python311Packages.djangorestframework
    pkgs.python311Packages.pandas
    pkgs.python311Packages.reportlab
    pkgs.python311Packages.corsheaders
    pkgs.nodejs_20
    pkgs.nodePackages.npm
  ];

  env = {
    PYTHONPATH = ".";
    DJANGO_SETTINGS_MODULE = "chemical_equipment.settings";
  };
}
