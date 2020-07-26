import os.path
import xml.dom.minidom
from dateutil.parser import parse as parse_date

class AppleHealthToGoogleFit():
    PATH_XML = os.path.join(os.path.dirname(__file__), ".cache", "apple_health_export", "export.xml")
    
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
             cls.__instance = AppleHealthToGoogleFit()
        return cls.__instance

    def __init__(self, path_xml=None) -> None:
        self.path_xml = path_xml if path_xml is not None else AppleHealthToGoogleFit.PATH_XML
        self.dom_tree = xml.dom.minidom.parse(self.path_xml)
        self.a_records = self.dom_tree.documentElement.getElementsByTagName('Record')

    def get_g_records_step_count(self):
        for a_record in self.a_records:
            if a_record.getAttribute('type') != 'HKQuantityTypeIdentifierStepCount': continue

            # After Apple Health data is exported, the datetime accuracy is reduced to second.
            # If Google Fit is installed on iPhone, the accuracy of datetime recoreded is up to nanosecond.
            # However, Google Fit only upload recent 3 or 5 days' data.
            # That's why this script is needed to backup historical health data.
            startTimeNanos = int(parse_date(a_record.getAttribute('startDate')).timestamp())*1000000000
            endTimeNanos = int(parse_date(a_record.getAttribute('endDate')).timestamp())*1000000000
            # modifiedTimeMillis = int(parse_date(a_record.getAttribute('creationDate')).timestamp())*1000
            value_intVal = int(a_record.getAttribute('value'))

            g_record = \
            {
                "dataTypeName": "com.google.step_count.delta",
                "startTimeNanos": startTimeNanos,
                "endTimeNanos": endTimeNanos,
                # "modifiedTimeMillis": modifiedTimeMillis,
                # "originDataSourceId": "",
                "value": 
                [
                    {
                        # "mapVal": [],
                        "intVal": value_intVal
                    }
                ]
            }
            yield g_record


if __name__ == '__main__':
    def test():
        point = []
        a2g_fit = AppleHealthToGoogleFit.get_instance()
        for p in a2g_fit.get_g_records_step_count():
            point.append(p) 
        print(len(point), point[0])

    test()
