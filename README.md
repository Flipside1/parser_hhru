##PARSER FOR HH.RU
___

####This parser uses [Selenium](https://github.com/SeleniumHQ/selenium) to parse data from the site.
####Also, this project uses [PostgreSQL](https://www.postgresql.org/) database.
___
___

####In order to use the database, you need to write in the __"configuration"__ file: 
    host = "Your_host"
    user = "Your_username" 
    password = "Password_from_your_database" 
    db_name = "Name_your_database"

___
___

####The parser can be configured as follows:
The lines change in the __"main"__ file
- 31.
            search_name = ['django', 'python', 'developer']
        ![](1.jpg)

        You can change the tags that will be used to search for vacancies
        Also, you can add new words separated by commas.
___

- 51.
            if ('Python' in element.text) or ('Django' in element.text):
        __"Python"__ and __"Django"__ can be replaced with any other words. These words are needed in order to filter out vacancies that do not have these words.
        You can also add additional words through __"or"__ and enclose them in parentheses.

___
___
####My social networks:
- [My Telegram](https://t.me/maxim_odintsov)
- [My GitHub](https://github.com/Flipside1?tab=repositories)
