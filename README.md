# inducks-custom-report
Get some descriptive statistics about your Disney comics collection on the Inducks.

The custom report consists in data in CSV format, bar plots and pie charts about character appearances, artists, writers, years of release and length of the stories.

## Dependencies

All the necessary libraries are listed in the *requirements.txt* file.

You can install them by running:

```
pip install -r requirements.txt
```

## Usage

- Run *main.py* and wait for the script to get all the necessary info about the stories that make up your collection (it can take a while).

     - When finished, it will automatically create a *collection.json* file and dump the data there.

- At that point, run *report.py*, which will create a *report* directory where the report will be saved.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/giovanni-cutri/inducks-custom-report/blob/main/LICENSE) file for details.
