import json
import config
import datetime


class Engine:
    """
    use this class to load rules from file and process signals by calling check_rule_for_signal(signal)
    """
    def __init__(self, rule_file_path):
        """
        @summary: constructor to initialize rule file and load it.
        @param rule_file_path: path to rule file path.
        """
        self.rule_file_path = rule_file_path
        self.rules = {}
        self.load_rules()

    @staticmethod
    def to_string(value):
        """
        @summary: Method to convert incoming value to string.
        @param value: any string value.
        @rtype: basestring
        @return: string value.
        """
        return str(value).lower()

    @staticmethod
    def to_integer(value):
        """
        @summary: Method to convert incoming string to float.
        @param value: any string value.
        @rtype: float
        @return: float value.
        """
        try:
            return float(value)
        except:
            return None

    @staticmethod
    def to_datetime(value):
        """
        @summary: Method to convert incoming string to datetime.
        @param value: any string value in %Y-%m-%d %H:%M:%S format.
        @rtype: datetime.datetime
        @return: datetime.datetime object.
        """
        try:
            if value == 'now':
                return datetime.datetime.now()
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            return None

    @staticmethod
    def greater_than(value, value_to_check):
        """
        @summary: Method to apply greater than operator on given operands.
        @param value: value in rules.
        @param value_to_check: value from signal.
        @rtype: bool
        @return: true if condition is true.
        """
        if value_to_check > value:
            return True
        return False

    @staticmethod
    def smaller_than(value, value_to_check):
        """
        @summary: Method to apply smaller than operator on given operands.
        @param value: value in rules.
        @param value_to_check: value from signal.
        @rtype: bool
        @return: true if condition is true.
        """
        if value_to_check < value:
            return True
        return False

    @staticmethod
    def equal_to(value, value_to_check):
        """
        @summary: Method to apply equal to operator on given operands.
        @param value: value in rules.
        @param value_to_check: value from signal.
        @rtype: bool
        @return: true if condition is true.
        """
        if value_to_check == value:
            return True
        return False

    @staticmethod
    def process_signal_data(signal):
        """
        @summary: Method to parse signal data.
        @param signal: signal from source.
        @rtype: bool
        @return: signal dict otherwise.
        """
        try:
            signal_dict = json.loads(signal)
            return signal_dict
        except:
            print 'signal invalid' + str(signal)
            return None

    def validate_signal(self, signal_dict):
        """
        @summary: Method to validate signal dict.
        @rtype: bool
        @return: True if valid and False otherwise.
        """
        try:
            for key in config.MANDATORY_SIGNAL_DATA:
                if key not in signal_dict:
                        return False
        except:
            return False
        return True

    def load_rules(self):
        """
        @summary: Method to load rules from rules.txt file.
        @rtype: bool
        @return: True if valid and False otherwise.
        @example: {'ATL6': {'Integer': [['>', 10.0], ['!=', 20]], 'String': [['=', 'HIGH']], 'Datetime': []}}
        """
        with open(self.rule_file_path, "r") as rules_file:
            for rule in rules_file:
                if not rule.startswith('#'):
                    try:
                        empty_rule = {'Integer': [],
                                      'String': [],
                                      'Datetime': []}
                        # replace newline character
                        rule = rule.replace('\n', '')
                        rule = rule.split(',')
                        if rule[0] not in self.rules:
                            self.rules[rule[0]] = empty_rule
                        #convert rule value and append in dict
                        self.rules[rule[0]][rule[1]].append([rule[2], self.data_type_to_value(rule[1], rule[3])])
                    except:
                        print "invalid rule " + str(rule)
        return

    def data_type_to_value(self, signal_type, *args):
        """
        @summary: Method to convert value based on given type.
        @param signal_type: string any one in the list used below
        @param args: values string object
        @rtype: basestring, float, datetime
        @return: corresponding type value
        """
        switch = {
            'String': self.to_string,
            'Integer': self.to_integer,
            'Datetime': self.to_datetime
        }
        return switch.get(signal_type)(*args)

    def rule_to_comparison(self, rule, *args):
        """
        @summary: Method to apply rule on given operands.
        @param rule: rule to be applied
        @param args: operands
        @rtype: bool
        @return: result of rule applied
        """
        switch = {
            '>': self.greater_than,
            '<': self.smaller_than,
            '!=': self.equal_to
        }
        return switch.get(rule)(*args)

    def check_with_rules_match(self, signal_name, signal_type, signal_value):
        """
        @summary: Method to check if signal got rules to apply and apply the rules.
        @param signal_name, signal_type, signal_value: signal values received
        @rtype: None
        @return: print signal name if it violates any rules
        """
        rules_to_check = self.rules[signal_name][signal_type]
        for rule in rules_to_check:
            if self.rule_to_comparison(rule[0], rule[1], signal_value):
                print signal_name

    def check_rule(self,signal_name, signal_type, signal_value):
        """
        @summary: Method to check if signal value_type is valid and signal got rules then proceed.
        @param signal_name, signal_type, signal_value: signal values received
        @rtype: None
        """
        if signal_name in self.rules:
            if signal_type in self.rules[signal_name]:
                if signal_type in config.ALLOWED_SIGNAL_VALUE_TYPE:
                    converted_value = self.data_type_to_value(signal_type, signal_value)
                    self.check_with_rules_match(signal_name, signal_type, converted_value)

    def check_rule_for_signal(self, signal):
        """
        @summary: Method to check if signal is valid and convert signal from string to dict then proceed.
        @param signal: signal as string or dict
        @rtype: None
        """
        if isinstance(signal, basestring):
            signal = self.process_signal_data(signal)
        if signal and self.validate_signal(signal):
            signal_name = signal['signal']
            signal_type = signal['value_type']
            signal_value = signal['value']
            self.check_rule(signal_name, signal_type, signal_value)
        else:
            print "unable to process"
