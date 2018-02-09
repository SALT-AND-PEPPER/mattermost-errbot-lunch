# Lunch Errbot plugin

This is a plugin for Lunch Dates for Errbot. The Idea is to communicate with (new) colleagues.
For that you add yourself to the participants list for the day. At 11:30 PM Err creates random 
groups(each group 4 Persons). There are two time-slots one at 12:00 and one at 12:20. See !help lunch_add
for details.

For more information about Errbot you can find it here: http://errbot.io
and here http://errbot.io/en/latest/user_guide/plugin_development/

## Installation

```bash
!repo install https://github.com/SALT-AND-PEPPER/LunchMattermost
```

## Example

```TypeScript
!lunch add 20 CP or !lunch_add CP 20 adds you to the 12:20 group with desired place: CP
!lunch add 20 adds you to the 12:20 group, place wherever
!lunch add CP adds you to the 12:00 group with desired place CP
!lunch add adds you randomly to one group
!help lunch for help
```

## License

The MIT License (MIT) Copyright © 2018 SALT-AND-PEPPER GmbH & Co. KG, https://www.salt-and-pepper.eu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


