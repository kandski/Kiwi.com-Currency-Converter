import sys
import argparse
from json import dumps
from storage import StorageAlchemy

class Converter():
    def __init__(self, storage):
        self.db = storage

    def cli_parse(self):
        self._args = argparse.ArgumentParser(prog='Converter', add_help=False)
        self._required = self._args.add_argument_group('Required arguments')
        self._required.add_argument('--amount', help='Amount of currency to convert',
                              required=True, type=float)
        self._required.add_argument('--input_currency', help='Currency to convert',
                              required=True)

        self._optional = self._args.add_argument_group('Optional arguments')
        self._optional.add_argument('-h', '--help', action="help", help='Show this help' )
        self._optional.add_argument('--output_currency',
                            help='Converted currency, when not present all known '
                                   'currencies are printed')
        self._optional.add_argument('-u', '--update', action='store_true',
                            help='Download and update database with rates')


        parsed_args = vars(self._args.parse_args())

        if parsed_args['update']:
            json = self.db.update_db()
            print(dumps(json, indent=4))
            sys.exit(0)

        return parsed_args

    def convert(self, in_curr_sym, out_curr, amount):
        in_curr = self.symbol_check(in_curr_sym)
        coefficient = self.db.get_coeficient(in_curr, out_curr)
        calculated = dict()
        for key, value in coefficient.items():
            calculated[key] = format(value * amount, '.2f')

        result = dict()
        result['input'] = {'amount': amount, 'currency': in_curr}
        result['output'] = calculated
        return result

    def symbol_check(self, symbol):
        for key, val in self.db.symbol.items():
            if symbol == val:
                return key
        return symbol

if __name__ == "__main__":
    c = Converter(StorageAlchemy())
    args = c.cli_parse()
    json = c.convert(args['input_currency'], args['output_currency'],
                     args['amount'])
    print(dumps(json, indent=4))
