#Senior Design Flask App 

#Requirements
- ImageMagick 6: https://legacy.imagemagick.org/script/download.php
- Venv (Use Python 3) https://docs.python.org/3/library/venv.html
- Pip https://pip.pypa.io/en/stable/installing/
- Zbar http://zbar.sourceforge.net/index.html

#First time setup
1. Create a master folder. This folder will contain all the files needed in order to run both applications.
2. Clone the ‘senior_design_v1’ and ‘batch_match_app’ repositories into the master folder.
3. In the master folder, at the same level as ‘senior_design_v1’ and ‘batch_match_app,’ also create a folder called ‘shared.’ Within shared, create five folders: ‘check’, ’temp’, ‘error’, ‘scanned’, and ‘nomatch’.
4. Create another directory called ‘venv’ within the master folder. Run `python3 -m venv venv` from the master folder. Start up the virtual environment by either running `. venv/Scripts/activate` (Windows) or `source venv/bin/activate`(Mac). For more information, see the link for ‘Venv (Use Python 3)’ above.
5. From the ‘senior_design_v1’ clone, run `pip install -r requirements.txt` to install all the python contained dependencies the program has.
6. From the ‘batch_match_app’ clone, run `pip install -r requirements.txt` to install all the python contained dependencies the program has.
7. In order to get the SSO and CAS Authentication to work, there is a simple edit that needs to be done. For Windows, go to ‘venv/Lib/site-packages/flask-cas/routing.py’ and add ‘or {}’ at the end of line 125. For Mac, go to ‘venv/lib/python3.7/site-packages/flask_cas/routing.py’ and change line 125 to: ‘attributes = xml_from_dict.get("cas:attributes") or {}’.
8. For Windows, in order for ImageMagick to work, you have to set a MAGICK_HOME environment variable to the path of ImageMagick. You can set it in Computer -> Properties -> Advanced system settings -> Advanced -> Environment Variables.
(E.g. New System Variable, Variable name: MAGICK_HOME, Variable value: C:\Program Files\ImageMagick-6.9.3-Q16)

#Running the program:
1. If it is not already running, start up the virtual environment by either running `. venv/Scripts/activate` (Windows) or `source venv/bin/activate`(Mac)
2. For Mac, to use ImageMagick, run `export MAGICK_HOME=/usr/local/opt/imagemagick@6`. Be sure that ImageMagick 6 is installed.
3. To start the exam request app, go into the ‘senior_design_v1’ folder and run `python run.py`.
4. The application will begin running on http://127.0.0.1:8080. You can access it using any browser.
5. To start the batch match app, open a second terminal window, repeat steps 1 and 2, go into the ‘batch_match_app’ folder, and again run `python run.py`
6. The second application will begin running on http://127.0.0.1:5000. You can access it using any browser.
