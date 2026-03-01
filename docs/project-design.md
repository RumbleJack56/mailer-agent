I want to design a project with the following features:

A Fastapi Backend
A next js frontend
A postgres db 
Google Oauth
JWT based Authentication and Authz

Authz done by role which is embedding in the JWT token itself
Roles customizable
FastAPI injection of user (using header) and require_role decorator check

Core Idea
Users can be added to groups by admins
Each group has a certain number of templates 

Template is determined by a prompt and some fillable fields
Each template is used to design an Email for a particular usecase

role >= user can use templates to draft mails
role >= Moderator can create and modify templates
role >= moderator can approve and send mails
role >= admin can add and remove users from groups and also create new groups
role >= admins can assign roles to users
role >= owner can create admins
Highest role is root.

Users cannot see any templates unless they are added to a group
A template is not linked to a group

User cannot see groups they are not part of
>= Admins can see other groups


User <-> Group is a many to many relation
Group <-> Template is a many to many relation

Each mail is inside a group, it has a creator, an approver (null initially), a subject, a body, and a list of recipients, and a source template id

FK relations are used properly to connect tables.

Frontend has the following pages:
- Landing
- Login/Register on same page
- Dashboard Page (groups for users, moderators; Extra features for admins like seeing all groups, create groups,etc)
- Groups Page (shows a specific group, its users on a collapsible panel on right, A templates )
- Sidebar on Left showing (Members, Templates, Mails, Notifications, Settings (for >=admins))
- When on mails page, user can see all previously sent mails and approval status
- User can start to create new mail by selecting a template and filling the field (**MORE IN MAILPAGE SECTION**)


### MAILPAGE SECTION

Create new mail leads to a new page

This page is dynamic.
It is divided into two sections. 
Left side is text fields and menus, right side is editable text Editor where mail body shows
Initially only left side is visible and is centered.
When a template is selected, the corresponding fields are shown, once the user fills the fields.
User clicks, generate draft. (the prompt + fields are send to backend, LLM calling is done and the response is shown on editor)
When user clicks genrate draft the left (which was centered) moves to the left and the right side is revealed.

User can edit the text and it shows in form of diffs (like git diffs)
and user can save draft, or send for approval. 

THe user has option to add additional information at the end of fields.

this is a dynamic page and is central to the application.


When Admin clicks on a mail to review, then the mail page is opened with the mail selected. and admin can see diffs, and also make edits before sending the mail finally.

Mail sending for approval creates notifications for the admins and moderators of the group. 
When a mail is sent, then user is sent a notification for the mail approval.


mail sending logic uses smtp and gmail id and app password, making it completely customizable. 
The app password is stored in the database and is used to send the mail.

The app password is encrypted by public key of backend and sent to backend. 

When mail needs to be sent, server decrypts with private key, and sends mail.




Template creation is also a feature of the system.
>= Moderators can create templates.

On template creation page, much like mail creation. 
Moderator or Admin starts creating a template, and determines which fields are needed. 
There is a fixed prompt which takes user input, asks some key questions to user (as mcq) and generates a finalized template which user can see, modify and then finally save. 
Once a template is saved, it can be added by >= Moderators to any group. 

When adding a template to a group, a moderator can only add templates they created, admins can add any template to the group. (they have a filter, made by me, made by others)


I want a specification document for each of the aspects of this project, from api design to db design to frontend design (colors, themes, elements), events and triggers and user flow.
