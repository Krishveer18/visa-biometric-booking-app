from app import db, Agent, app
from werkzeug.security import generate_password_hash

def add_agents():
    agents = [
        {'username': 'admin', 'password': 'admin'},
        {'username': 'agent1', 'password': 'password1'},
    ]
    for agent in agents:
        if not Agent.query.filter_by(username=agent['username']).first():
            new_agent = Agent(
                username=agent['username'],
                password_hash=generate_password_hash(agent['password'])
            )
            db.session.add(new_agent)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        add_agents()


