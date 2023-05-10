from get_data_classes import *
from src.utils import printj

hh = HeadHunterAPI()
hh.get_vacancies("python")
printj(hh.vacancies)
