from ..api import unifi, untis

'''
Example of user provisioning with pyunifi and webuntis
This example uses the webuntis library to get a list of students and then adds them to the Unifi controller as radius users.
When implementing this, you should change the password to a secure one and work out logic to select the BYOD students only.
'''

for student in untis.students():
    unifi.add_radius_user(student.full_name.replace(' ', '_'), "supersecurepassword")