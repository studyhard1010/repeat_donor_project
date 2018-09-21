import sys
import time
import math


def validate_other_id(other_id):
    return other_id == ""


def validate_cmte_id(cmte_id):
    return cmte_id != ""


def validate_trans_amt(amt):
    return amt.isdigit()


def validate_zipcode(zipcode):
    return len(zipcode) == 5 and zipcode.isdigit()


def validate_trans_date(dt):
    try:
        time.strptime(dt, "%m%d%Y")
    except:
        return False
    return True


def is_most_recent_donate(previous_time, present_time):
    return time.strptime(previous_time,  "%m%d%Y") < time.strptime(present_time,  "%m%d%Y")


class DonorRecord:
    """
    build the donor record
    should contains: CMTE_ID, ZIP_CODE and TRANSACTION_DT
    """

    def __init__(self):
        self.zipcode = ''
        self.cmte_id = ''
        self.trans_dt = ''
        self.record_amt = 0

    def add_donation(self, zipcode, cmte_id, trans_dt, amt):
        self.zipcode = zipcode
        self.cmte_id = cmte_id
        self.trans_dt = trans_dt
        self.record_amt = amt

    def get_cmte_id(self):
        return self.cmte_id

    def get_zipcode(self):
        return self.zipcode

    def get_transaction_yr(self):
        return self.trans_dt[-4:]

    def get_transaction_date(self):
        return self.trans_dt

    def get_last_record_amount(self):
        return self.record_amt


class Doner:
    """
    read from file and create donor objects
    """

    def __init__(self, input_path1, input_path2, output_path):
        self.input_file1 = input_path1
        self.input_file2 = input_path2
        self.output_file = open(output_path, 'w')
        self.donor_dict = {}
        self.repeat_donation_num = 0
        self.output_sequence = []
        self.output_amt_collector = []
        self.output_amt_sum = 0

    def __del__(self):
        self.output_file.close()

    """
    formula to calculate the n-th percentile:
    sample_list[ceiling(n / 100 * len(sample_list))- 1]
    """

    def get_percentile(self):
        idx = int(math.ceil(1.0 * self.percentile /
                            100 * len(self.output_amt_collector))) - 1
        return str(self.output_amt_collector[idx])

    def get_total_repeat_contribution(self):
        return str(self.output_amt_sum)

    def get_repeat_donation_num(self):
        return str(self.repeat_donation_num)

    """
    for list insertion in an increasing order
    """

    def add_to_output_collection(self, amt):
        l = len(self.output_amt_collector)
        if l == 0:
            self.output_amt_collector = [amt]
        else:
            for i in range(l):
                if self.output_amt_collector[i] > amt:
                    self.output_amt_collector.insert(i, amt)
                    break

                if i == l - 1:
                    self.output_amt_collector.append(amt)

    def run(self):
        """
        for reading input_file1 and update donor record
        output to file afterwards
        """

        # get percentile
        file2 = open(self.input_file2, 'r')
        self.percentile = int(file2.readlines()[0])
        file2.close()

        # read from donation list
        with open(self.input_file1) as f:
            for line in f:
                CMTE_ID, NAME, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = self.parse_line(
                    line)
                if validate_cmte_id(CMTE_ID) and validate_other_id(OTHER_ID) and validate_trans_amt(TRANSACTION_AMT) and validate_zipcode(ZIP_CODE) and validate_trans_date(TRANSACTION_DT):
                    self.update_donor_record(NAME, CMTE_ID, ZIP_CODE,
                                             int(TRANSACTION_AMT), TRANSACTION_DT)

        for donor_name in self.output_sequence:
            add_amt = self.donor_dict[donor_name].get_last_record_amount()
            self.output_amt_sum += add_amt
            self.repeat_donation_num += 1
            self.add_to_output_collection(add_amt)
            self.output_to_file(donor_name)

    def parse_line(self, line):
        """
        parse the lines and return the contents in the following columns:
        CMTE_ID
        NAME
        ZIP_CODE
        TRANSACTION_DT
        TRANSACTION_AMT
        OTHER_ID
        """
        cols = line.split("|")
        return cols[0], cols[7], cols[10][:5], cols[13], cols[14], cols[15]

    def update_donor_record(self, donor_name, cmte_id, zipcode, amt, trans_dt):
        """
        add donor record if donor does not exist
        otherwise, it means there exists a repeat donor
        then aggregate the repeat donoation amount
        """
        if donor_name not in self.donor_dict:
            # for first time donor
            self.donor_dict[donor_name] = DonorRecord()
            self.donor_dict[donor_name].add_donation(
                zipcode, cmte_id, trans_dt, amt)
        else:
            # for repeat donors
            if donor_name not in self.output_sequence:
                # first time repeat donor
                self.output_sequence.append(donor_name)

            if is_most_recent_donate(self.donor_dict[donor_name].get_transaction_date(), trans_dt):
                # update existed donor most recent record
                self.donor_dict[donor_name].add_donation(
                    zipcode, cmte_id, trans_dt, amt)

    def output_to_file(self, donor_name):
        """
        write to output with formating
        """
        data = self.donor_dict[donor_name]
        cols = [data.get_cmte_id(), data.get_zipcode(), data.get_transaction_yr(),
                self.get_percentile(), self.get_total_repeat_contribution(), self.get_repeat_donation_num()]
        self.output_file.write("|".join(cols) + "\n")


if __name__ == "__main__":
    """
    read from bash, get:
    input1_path
    input2_path
    output_path
    """
    d = Doner(sys.argv[1], sys.argv[2], sys.argv[3])
    d.run()
