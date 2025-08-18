from sqlmodel import Session, select, or_, col, delete
from app.models.hero_model import Hero
from app.models.team_model import Team
from db.database import engine, create_db_and_tables

def create_teams(teams: list[Team]):
    with Session(engine) as session:
        session.add_all(teams)  # This will add both teams to the session
        session.commit()  # This will commit the changes to the database, saving the teams to the database
        for team in teams:
            session.refresh(team)
    return teams

def create_heroes(heroes:list[Hero]):
    with Session(engine) as session:
        session.add_all(heroes)
        session.commit()
    return heroes

def select_heroes():
    with Session(engine) as session:

        statement = select(Hero).where(Hero.name == "Deadpond")  # This will select all heroes and their associated teams
        results = session.exec(statement)
        hero = results.one_or_none()
        if hero:
            print(f"Hero found: {hero.name}, Secret Name: {hero.secret_name}, Age: {hero.age}")

def select_heros_and_team_names():
    with Session(engine) as session:
        # statement = select(Hero.id, Hero.name, Team.name).join(Team, onclause=(col(Hero.team_id) == col(Team.id))).where(col(Team.id) > 1)  # a way to do it using col
        statement = select(Hero, Team).join(Team, isouter=True)# This will join the Hero and Team tables on the team_id foreign key, is outer is equal to LEF OUTER
        results = session.exec(statement)
        # print(results.all())  # This will print all heroes and their associated team names
        for hero, team in results:
            print(f"Hero: {hero.name}, Team: {team.name if team else 'No Team'}")


def update_heros():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero = results.one()
        print(f"Hero before update: {hero}")
        hero.age = 16
        print(f"Hero after update: {hero}")
        session.add(hero)
        session.commit()  # This will commit the changes to the database, updating the hero's
        session.refresh(hero)  # This will refresh the instance with the latest data from the database
        print(f"Hero after refresh: {hero}")

def update_heros_team(hero_name: str, new_team: Team | None):
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == hero_name)
        results = session.exec(statement)
        hero = results.one_or_none()
        if hero:
            print(f"Hero before update: {hero}")
            hero.team = new_team
            session.add(hero)
            session.commit()
            session.refresh(hero)  # This will refresh the instance with the latest data from the database
            print(f"Hero after update: {hero}")

def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Man")
        results = session.exec(statement)
        hero = results.one_or_none()
        if hero:
            session.delete(hero)
            session.commit()
            print(f"Hero {hero.name} deleted successfully.")
        else:
            print("Hero not found, nothing to delete.")     # For example when we said something like Spider-Boyy or Spider-Boy1 it will not find the hero and will not delete anything
            
def clear_tables():
    with Session(engine) as session:
        statement = delete(Hero)  # This will delete all heroes from the database
        session.execute(statement)  # This will execute the delete statement
        statement = delete(Team)
        session.execute(statement)  # This will execute the delete statement
        session.commit()

def add_hero_to_team(hero_name:str, team_name: str):
    with Session(engine) as session:
        # Obtain the hero from the database
        hero_statement = select(Hero).where(Hero.name == hero_name)
        hero = session.exec(hero_statement).one()

        # Obtain the team from the database
        team_statement = select(Team).where(Team.name == team_name)
        team = session.exec(team_statement).one()

        # Add hero to team
        team.heroes.append(hero)  # This will add the hero to the team's heroes list
        session.add(team)  # This will add the team to the session
        session.commit()
        session.refresh(team)  # This will refresh the team instance with the latest data from the database

def delete_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Z-Force")
        team = session.exec(statement).one()
        session.delete(team)  # This will delete the team and all associated heroes due to cascade_delete=True
        session.commit()
        print(f"Team {team.name} deleted successfully, along with all associated heroes.")

def main():
    create_db_and_tables()  # This will create the database and tables if they do not exist
    clear_tables()  # This will clear the tables before creating new teams and heroes
    print("Tables cleaned successfully.")
    print("Starting to create teams and heroes...")

    teams_data = [
    Team(name="Preventers", headquarters="Sharp Tower"), 
    Team(name="Z-Force", headquarters="Sister Margaret's Bar")
    ]

    create_teams(teams_data)  # This will create some teams in the database
    print("Teams created successfully.")

    heroes_data = [
    Hero(name="Deadpond", secret_name="Dive Wilson", team=teams_data[0]),  # If teams is not None, assign the id of the first team to team_id, otherwise assign None
    Hero(name="Spider-Boy", secret_name="Pedro Parqueador", team=teams_data[0]),  # If teams is not None, assign the id of the second team to team_id, otherwise assign None
    Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=teams_data[1]), # If teams is not None, assign the id of the first team to team_id, otherwise assign None
    Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32, team=teams_data[0]),
    Hero(name="Black Lion", secret_name="Trevor Challa", age=35, team=teams_data[1]),
    Hero(name="Dr. Weird", secret_name="Steve Weird", age=36, team=teams_data[0]),
    Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)
    ]

    print("Starting to create heroes...")
    create_heroes(heroes_data)  # This will create some heroes in the database
    print("Heroes created successfully.")
    # select_heroes()  # This will select and print all heroes from the database
    # print("Heroes selected successfully.")
    # update_heros()  # This will update the heroes in the database
    # print("Heroes updated successfully.")
    # delete_heroes()  # This will delete the heroes in the database
    # print("Heroes deleted successfully.")
    # select_heros_and_team_names()  # This will select and print all heroes and their associated team names from the database
    # print("Heroes and their team names selected successfully.")
    # update_heros_team("Captain North America", teams_data[0])  # This will update the team of Captain North America to the first team
    # # In the time captain America decides to get out of the team, we can set the team_id to None
    # update_heros_team("Captain North America", None)  # This will update the team of Captain North America to None
    # print("Heroes team updated successfully.")
    # # Now Captain North America is not part of any team, so we can add him to a team later if we want
    # add_hero_to_team("Captain North America", "Z-Force")  # This will add Captain North America to the Z-Force team
    # print("Captain North America added to Z-Force team successfully.")
    # delete_team()  # This will delete the Z-Force team and all associated heroes


if __name__ == "__main__":
    main()  # This will run the main function when the script is executed