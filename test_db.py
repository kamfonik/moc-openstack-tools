import model

new_request = model.Request(first_name='Laura', last_name='Kamfonik', email='a_fake_email')
model.db.session.add(new_request)
model.db.session.commit()

new_user = model.NewUser(new_request, 'my_username', 'my_org', 'my_role', 'my_sponsor', '1234', 'testing new users')
model.db.session.add(new_user)
new_proj = model.NewProject(new_request, 'my_project', 'facts about my project', 'user1@moc, user2@moc')
model.db.session.add(new_proj)
model.db.session.commit()

