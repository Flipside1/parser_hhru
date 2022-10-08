## PARSER FOR HH.RU
___
### What this parser can do:
    
- Collects vacancy titles and links to them.
- Collects company names.
- Collects information about required work experience.
- Collects information about the skills required for the job.
- Inserts all collected data to "PostgreSQL" database.
___
### What technologies are used in this project:
- This parser uses ___[Selenium](https://github.com/SeleniumHQ/selenium)___ to parse data from the site.
- Also, this project uses ___[PostgreSQL](https://www.postgresql.org/)___ database.

___

#### In order to use the database, you need to write in the __"configuration"__ file: 
    host = "Your_host"
    user = "Your_username" 
    password = "Password_from_your_database" 
    db_name = "Name_your_database"

---

#### The parser can be configured as follows:
The lines change in the __"main"__ file.

- __31 string__:

      search_name = ['django', 'python', 'developer']

    - You can change the tags that will be used to search for vacancies.
    - Also, you can add new tags separated by commas.


- __51 string__:

      if ('Python' in element.text) or ('Django' in element.text):
     __"Python"__ and __"Django"__ can be replaced with any other tags. These words are needed in order to filter out vacancies that do not have these words.
     You can also add additional words through __"or"__.

___

#### My social networks:
- [My Telegram](https://t.me/maxim_odintsov)
- [My GitHub](https://github.com/MaximOdintsov?tab=repositories)
