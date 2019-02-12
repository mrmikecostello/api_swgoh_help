# api_swgoh_help
Python wrapper for the API at https://api.swgoh.help/

## Usage

          from api_swgoh_help import api_swgoh_help, settings

          creds = settings('your_username','your_password')
          client = api_swgoh_help(creds)

#careful, allycode is integer, not string
          
          allycode = 123456789

