from sqlmodel import Session, select, or_, col, delete
from app.models.basemodels import Team, Hero, engine, create_db_and_tables

teams = [
    Team(name="Preventers", headquarters="Sharp Tower"), 
    Team(name="Z-Force", headquarters="Sister Margaret's Bar")
    ]

heroes = [
    Hero(name="Deadpond", secret_name="Dive Wilson", team_id=teams[1].id if teams else None),  # If teams is not None, assign the id of the first team to team_id, otherwise assign None
    Hero(name="Spider-Boy", secret_name="Pedro Parqueador", team_id=teams[0].id if teams else None),  # If teams is not None, assign the id of the second team to team_id, otherwise assign None
    Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team_id=teams[0].id if teams else None), # If teams is not None, assign the id of the first team to team_id, otherwise assign None
    Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32, team_id=teams[1].id if teams else None),
    Hero(name="Black Lion", secret_name="Trevor Challa", age=35, team_id=teams[1].id if teams else None),
    Hero(name="Dr. Weird", secret_name="Steve Weird", age=36, team_id=teams[1].id if teams else None),
    Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)
    ]

def create_teams(teams: list[Team]):
    with Session(engine) as session:
        session.add_all(teams)  # This will add both teams to the session
        session.commit()  # This will commit the changes to the database, saving the teams to the database
    return teams

def create_heroes(heroes:list[Hero]):
    with Session(engine) as session:
        session.add_all(heroes)
        session.commit()
    return heroes

def select_heroes():
    with Session(engine) as session:

        statement = select(Hero).where(col(Hero.age) > 32).offset(0).limit(2)     # This will select the first 3 heroes from the database, skipping the first 3 heroes 3 by 3 going through the list when we said
                                                        # OFFSET 5 LIMIT 3 it means skip the first 5 and get the next 3 so it will return heroes with id 6,7 and 8 but now we don't have 8
                                                        # Only heroes with id 6 and 7 will be returned
        results = session.exec(statement)

        # hero = session.get(Hero, 100)  # This will get the hero with id 1 from the database, if it exists
        #print(f"First Hero: {results.first()}") # This will print the first hero from the results
        # print(f"One Hero: {results.one()}") # This will print one hero from the results, if there are multiple heroes it will raise an error
        # for hero in results:  # This will iterate over the results and print each hero
        #     print(hero)
        heroes = results.all()            # This will get all the heroes from the database in list format
        # print("Heroes in the database:")
        print(heroes)
        
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

def main():
    create_db_and_tables()  # This will create the database and tables if they do not exist
    clear_tables()  # This will clear the tables before creating new teams and heroes
    print("Tables dropped successfully.")
    print("Starting to create teams and heroes...")
    create_teams(teams)  # This will create some teams in the database
    print("Teams created successfully.")
    print(teams)
    print("Starting to create heroes...")
    create_heroes(heroes)  # This will create some heroes in the database
    print("Heroes created successfully.")
    select_heroes()  # This will select and print all heroes from the database
    print("Heroes selected successfully.")
    update_heros()  # This will update the heroes in the database
    print("Heroes updated successfully.")
    delete_heroes()  # This will delete the heroes in the database
    print("Heroes deleted successfully.")


if __name__ == "__main__":
    main()  # This will run the main function when the script is executed