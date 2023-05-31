# check_knot_statistics - Icinga / Nagios Plugin to check Knot DNS statistics

Goal of this check script is to read Knot DNS statistics and return it so we can collect some relevant performance data over time and e.g. visualize it via Grafana.

## Installation (Icinga2):
to be written
## Command Line Options:

| Option | Triggers what?                                                                          | Mandatory? | Default value |
|--------|-----------------------------------------------------------------------------------------|------------|---------------|
| -h     | Renders the help / usage information                                                    | no         | n/a           |
| -f     | The path to the Knot statistics YAML file | yes        | n/a           |

Hint: The statistics file on Ubuntu is usually at `/var/run/knot/stats.yaml`

## TODO:
Well, it needs some serious testing to be honest - please provide feedback on whether the plugin helped and in which environment you tested it.

And currently it always returns OK and some numbers. As long as the statistics file can be parsed, there's nothing that would result in a WARNING or CRITICAL state, this could e.g. be extended to check for failures or too high number of queries.


## How to contribute?
Feel free to [raise a new issues](https://github.com/mrimann/check_knot_statistics/issues) if you find a problem or to propose a new feature. If you want to contribute your time and submit an improvement, I'm very eager to look at your pull request!

In case you want to discuss a new feature with me, just send me an [e-mail](mailto:mario@rimann.org).


### Contributors / Supporters
Thanks for your support! (in chronological order)
- [internezzo ag](https://www.internezzo.ch/) for sponsoring the initial development

## License
Licensed under the permissive [MIT license](http://opensource.org/licenses/MIT) - have fun with it!

### Can I use it in commercial projects?
Yes, please! And if you save some of your precious time with it, I'd be very happy if you give something back - be it a warm "Thank you" by mail, spending me a drink at a conference, [send me a post card or some other surprise](http://www.rimann.org/support/) :-)
