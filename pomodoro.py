import base64
import os
from PyQt5 import QtWidgets, QtCore, QtGui
import signal
import sys
import tempfile
import time

WORK_IMAGE = """iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAMAAABOo35HAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAdRQTFRFAAAAX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78AX78A////MaP1EQAAAJp0Uk5TAAABCBIcL0tfcIKTpbbH1dzh5+zy9/wDDjlYcoukvdbm7vT5/gYVLVBzl7rb7QodQ6DN6AkhUYGv2vH9OKn1BVKNxQQblhlP0gyGzh9isOo+Eaq78yJ0y/h20/tx0BpszPpcxgdBriuS6RbZRO/JgLULaN6UM7hTD3mcKbM6Ak7XZIn2keXYVOtp3UwjyB4sIM/KP45h1PBZvpwMqOAAAAABYktHRJvv2FeEAAAACXBIWXMABOheAAToXgFkT/88AAAN7ElEQVR42u2diV9STReA7wF3NFQEMTQV0CgLKisryCXN1FxSEzVNU9LSNLXMxFzSbN+39337/trvgkugLAPce8/cyzx/wZnnd2bu3Jk5MxyHDKjUKalp6RmZWZrsnCPa3Lx8XYHeYNAX6PLzcrVH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"""

REST_IMAGE = """iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAYAAAB5fY51AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAHP4AABz+AFE9vraAAAACXZwQWcAAAEsAAABLAD7OHJpAAAaNklEQVR42u3de4zdZZ3H8fec3ui0AgUppQUEiiAQLgnKzY24KIJG0RizXkFX16gYw7oqG3FVvGHWy7rGWDWuN3C9xRhFo+AFxazclAQhgCAFRGlLofRiO7QzbWf/+P7m9JnDdObMzPmd5/c75/1KJoNYZp7f7/T55Ps8v+d5fgOor43GtwFgATBYfB0IHAo8FVgCHNDyfQmwb/HfzAPmt3yfV/z4keJruOX7DmALsLH4erzl+2PA34ANwFDxtQMYHch9w5SVn3+fKIJpDrCICJvDgKcBy4FDWr72B/ZhfACV/XdllPEBtx3YBKxt+VoD/AX4KxF624Bd/kXuD37OPWZ0zz/OB/YDlgEri6+ji+9HEtXSIFEl1eXvwShRaQ0R1dgDwGrgvuL7amAdsJkIvdpcmNrj51lzyZBuITGUOwY4GTgJOBFYASwmwqlXP+9RIsS2Ag8DdwC3A38E7iWGlk/gkLL2/PxqJqmgFhLV0ynF10nACcDBREA1crc1s91EgD0C3EkE2G3F1zoiwOwANePnVQPJ/NN+RAV1BnAmcCox5zSYu401MUTMg90K3AjcRFRgm3EerBb8jCqqCKl5RBX1LODZRFAdS0yKz8ndxprbRUzq30ME1++A3xPV14gdo5r8XCqkCKm5xLDudOD5wNnAEVhFlW0IeBC4HvglcDMxnNxpJ6kOP4vMkuHeUuA09oTUSgypXIaIJ45j4XULsB6Hjdl5/zNIJs4XE0/yXgKcT8xPLcrdPo2zjZjnugb4MfEEcivYeXLwnndRMuRbATwPuAA4i1hR7mdRbaPECvwbgKuBXxFLKBwydpH3umRJNTUIPBN4KVFNHU0s7lT9DBOLVa8BfgT8gRhG2qFK5v0tSRJUS4g5qdcA5xArzL3vvWGUWHF/HfAtYs5rI/gBl8X72mHJyvNlwAuBVxPLERbnbptKtZVYHvFt4GfE8ghX1neY97NDkqA6Eng58EpiQn1B7rapq3YQE/PfBX5A7Hc0uDrE+zhLSVAdToTUhcAziMl19a+dwJ+Aq4jwegiDa9a8fzOUBNWhwCuA1xN7+QwqpXYSexm/AXyfOOfL4Joh79s0JZPpy4mh3xuIjcfzZvQD1S9GiA3YXyeGimvADjhd3q82JUG1L7F+6mJi87FLEzQdw8Tm61XEeq4tYEdsl/epDUVYLSAWeb4DOA+3zWh2hoBrgc8Ri1F32Bmn5j2aRDJPdTzwFmJSfWnudqmnrCcm5b8E3IXzW5Py3kwgGf4tBS4C3gw8He+XyjEK/Bn4MnAlEWL+ZZuA96RFcg7V2cClxXfnqdQNw8Rq+U8U3z2Xq4X3o5BUVYcBbwPehMM/5bEe+ArwBeLtQHbUgveBZljtQ2xKvpQ4l8oTPZXTLuIcrk8Qm6y321n7PLCSquoo4J3A64jjh6Wq2AR8E/gMcD/0d6ft22tP5qpeAHyAODe9b++HKm2UOG/+w8DP6eO5rb677qSqOgh4O7EA9KDc7ZLa8Cix4PTzxT/3XQfuq+tN1lWdDrwfOBe31KheRoBfAB8hXpTRV+u2+uZai7BaRJymcClxDIxUVw8QE/JXAdv6pSP3/HW2bFa+jNis7Ise1Au2EZupr6BPNlP39PUlYXUq8DFiCNjvr3BXb9lNDBHfR2yq7ulO3bPXljwFvIB4unJ87jZJJbqLeNp9NT38FLEnr6sIq/2IJ4DvAg7M3SapCzYAnyaeJG7uxc7dU9eUDAFXAB8CXkusYJf6xXbgf4EPEu9N7KlO3jPXkoTVccTTkxfhfJX6027gp8TT8Luhdzp6T1xHElZnAZ8CzszdJqkCbgTeTRwQ2BOdvfYVyOie67iA2OFuWEnhTKJPXAA0Rmf5w6qg1oFVfADzgTcCXyReryVpj2cQfeONwPy6h1Ztq8TkSJiLiW02++duk1Rhm4jtPKuo8VE1tWx3EVaDwCXAe4Gn5G6TVAN/Bz4OfBYYqmPnr12bi7BaDLyHWGPlNhupfduItVqfBLbWLQBq1d5kQehlxOu2FuZuk1RDTxCvF7uCmi0wrU1bi7BaAlxOvHJrQe42STW2g3i12OXAxroEQS3amVRWHwbeim+xkTphmHiC+AFqUmlVfllDMmd1GVFZGVZSZ8wn+tRlwOI6LHmodGAlTwPfQ8xZOQyUOmsB0bfeAwxWPbQqG1jJOqtLiKeBTrBL5VhI9LFLgH2qHFqVDKxkBfvFxDorly5I5VpE9LWLqfCK+MoFVrI38CLgP3BRqNQtTyH63EVUdO9hpR4MJDfoAuI13ctzt0nqQ2uAtxGnl1YqJCrTlpYjYr4KHJu7TVIfu4fYMF2po2kqMSRsOXzvUxhWUm7HEn3xOBjXR7OqRGAVVhAnhXqelVQNZxJ9ckXuhozJHljJKvYPEccaS6qOFxF9c78qVFlZA6u4AXOJR6mvy90eSU/SIPrmxcDc3KGVLSCSC38Z8G+4il2qqgVEH30Z5J3PyjL53/JG5qsoJvYkVdrdwIVkfMN0ziHYCuL18YaVVA/HEX022yR81wOrqK7GtgGcm+vCJc3IuRTb5XIMDbsaWMUFDhBL//+5279f0qw1iL57ETDQ7dDq2jA0ubAziFdpH9Xla5XUOfcDrwVugu4FSbcrnKXEK7kMK6nejiL68tJu/tKuBFbLeqsXdPMCJZXmBXR5fVbpgZVcyPljF9ela5NUrrEi5Hzozvqsbg0JVxLn7BzUpd8nqTsOIvr2ym78slIDq0jcBcC/Aqd144Ikdd1pRB9fUHaVVVpgJQ1/IbEXqSpH6kjqrAGij78Qyh0alj0kPBy4FNi/5N8jKa/9ib5+eJm/pJTASp4KvhU4vcwLkFQZpxN9vrSnhh0PrKShzyWOWHU1u9QfGkSffy6UMzQsK0yWEuXhwSX9fEnVdDDR90tZUNrRwGrZK/iP5d4XSRX1j5S017CMCusE4F9wgajUr+YSGXBCp39wxwKrSNJ5wJvxrTdSvzuWyIJ5nayyOhJYSYP+AXhVN++KpMp6FZEJHZuA7+SQcF/gHXR597akylpKZMK+nfqBsw6sltfLn5fhpkiqrvOIbOhIldWpCms5sWt7MNNNkVRNg0Q2LO/ED5tVYCWJ+XLgmRlviqTqeiaREbOusjpRYR0GvJ54QihJreYRGXHYbH/QjAMrScpXAKfkviOSKu0UIitmVWXNtsI6gljR6iJRSZOZS2TFEbP5ITMKrCQh/wk4MfedkFQLJxKZMeMqazYV1lHEoV1zct8FSbUwh8iMGb81a9qB1fJk8Pjcd0BSrRzPLJ4YzrTCWk6UdlZXkqZjDpEdM1qXNa3Aanll18m5r1xSLZ3MDF8NNpMKawnwamB+7quWVEvziQxZMt3/sO3ASpLwbOCM3FcsqdbOILJkWlXWdCusQeA1wOLcVyup1hYTWTKt/cfTDaxnAefkvlJJPeEcIlPa1lZgje75sy8FDsx9lZJ6woFEpjTaHRZOp8I6DM+7ktRZ5zGNTdFTBlaSfOcAR+e+Okk95WiKaaZ2qqx2K6xFROnmUgZJnTSfyJZF7fzhdgPrZOCs3FcmqSedRZsL0ScNrOTFqC8GDsp9VZJ60kFExkz54tV2KqxlFMvoJakk5xNZM6l2Aus04JjcVyOppx1DZM2k9hpYRWk2B3g+bU6ISdIMLSKyZs5kw8KpKqxlFPt9JKlkZzPFsHCqwDodWJn7KiT1hZVE5uzVhIFVlGRziRLNl6NK6oZBInPm7m1YOFmFdQjwnNxXIKmvPIfInglNFljPAo7M3XpJfeVIJjnB4UmBlSwWfTYOByV11yCRPRMuIt1bhbUETxWVlMcZ7OX45L0F1jHAsblbLakvHcteFquPC6ykBDsDOCB3qyX1pQMoRnitw8KJKqyFwJnEPJYkddsAkUELW/+PiQJrGXBq7hZL6munMsGq94kC6xQmWQchSV1wCJFF4zQDKxkrnoLLGSTlNUgRWOk8VmuFtQg4KXdLJYnIonEnxbQG1gHACblbKUlEFo1brdAaWMcAS3O3UpKILBq3HqsB48aIJwP75W6lJBFZdDLsyai0wpqP81eSquUkktcLpoG1H3Bi7tZJUuJEklFfGljLgBW5WydJiRUkC0jTwFoJLM7dOklKLCY5pr2RTLivxLfjSKqWRRSBNcqeCmsOcHTulknSBI4mMqoZWM0Uk6SKaY7+xgJrXzy/XVI1HUlkVDOwDsMD+yRV0wFERjUD6wg8oUFSNQ0SGdUMrEOAfXK3SpImsA/FGX1pYElSVTUDq5leklRRhwD7NIjx4fLcrZGkSSwHBscCa9ksf5gklWkZRWAdCOyfuzWSNIn9gQMbwKH4hFBSte0DHNoAnkpyQJYkVdB84KkNYAkwL3drJGkS84AlDWLZu4ElqcrmAQeMVVgDuVsjSZMYIKmwJKnqmhWWJFXdEgNLUl0saVAcjCVJFbdvA1iQuxWS1IYFDVzSIKke5jVwlbukephvhSWpLqywJNWGFZak2phnYEmqi3mN2f8MSeqOBjCSuxGS1IYRA0tSXYw0gOHcrZCkNgxbYUmqCyssSbVhhSWpNkYawI7crZCkNuxoAFtyt0KS2rClAWzM3QpJasNGA0tSXWxsAI/nboUkteHxsQprNHdLJGkSoyQVlksbJFXZCEmFZWBJqrIRigrrMVztLqnahoHHGsDfgO25WyNJk9gO/K0BbAA25W6NJE1iE7ChAQwB63K3RpImsQ4YGgusNblbI0mTWEMRWNuBtblbI0mTWAtsbyT/Q5Kqai3ESyjG/odPCiVVUXMUOBZYDxJzWZJUNUNERjUD66+4CVpSNT1OZFQzsLYAD+RulSRN4AGKg0bHAmsbsDp3qyRpAquJjGoG1i7gvtytkqQJ3EdkFI2BPf+ymWKSVBHN0d8Aeyosin+5NXfrJCmxlWS6Kg2sdcDDuVsnSYmHSfY6p4G1Gbgjd+skKXEHkU3A+MAaBm7P3TpJStxOcsBoA2Iyq/BHkjSTpIw2E5nUzKhGyx+4F1ifu5WSRGTRvem/aA2sx4E7c7dSkogsGrdlsDWwtuE8lqRquJ2WtaHNwErmsW7Dkxsk5TVEZFGaTU+qsCj+kAf6ScppLUVgpSYKrHXArblbK6mv3coEL8eZKLCeAG4k3mUvSd02SmTQE63/x7jASsaKN+GBfpLyeJzIoHHzVzBxhQWx9uGe3K2W1JfuoWX91Zi9BdZGioSTpC67icigJ3lSYBUl2CjwO1zeIKm7hojsGR2Y4P9sTPIf/h7PeZfUXQ8Q2TOhyQJrLfDb3K2X1Fd+yyTrQCcMrKIU2wn8EoeFkrpjiMicnQN7+QONKX7Azfg2HUndsZrInL2aKrDWAdfnvgpJfeF6JljdntprYBUl2S6iRPNtOpLKtI3Iml0Dk/yhqSosgFvYyyIuSeqQe4msmVQ7gbUOuCb31UjqadcwxXAQpgisZBHpT4BHc1+RpJ70KJExowNT/MF2KiyIg+BvyH1VknrSDRQvm5hKu4G1DfgRyet2JKkDholsaevB3pSBlZRo1wH35b46ST3lPiJbmGo4CO1XWAB/Ba7NfXWSesq1RLa0pa3AKpJvN1G6bch9hZJ6wgYiU3a3U13B9CosiF3U1+W+Skk94TomOZlhItMNrCHgW8DW3Fcqqda2ElkyrcMV2g6spGS7Hk8jlTQ7N1HsU253OAjTr7Agji79Ni5xkDQzw0SGbJzufzitwEqS8BraXOglSS3+SLHdbzrVFcyswgJYA3yPOM1Bktq1i8iONTP5j6cdWEki/gC4K/fVS6qVu4jsmHZ1BTOvsADuB76JVZak9uwiMuP+mf6AGQVWkozfA+7IfRck1cIdRGbMqLqC2VVYAA8CVxIvrJCkvdlJZMWDs/khMw6sJCG/D9yW+25IqrTbiKyYcXUFs6+wIDYufgMYyX1HJFXSCJERbW9y3ptZBVbLE8M/ZL4pkqrpD8ziyWCqExUWxJqKVfjSVUnjDRHZMKN1V61mHVhJYl6N52VJGu9aIhtmXV1B5yosgC3A54D1GW6KpOpZT2TClk79wI4EVpKc/wd8p8s3RVI1fYfIhI5UV9DBCqto0AjwZeCe7t4XSRVzD5EFI50KK+jskHDMncD/4GJSqV/tJDLgzk7/4I4GVvLi1SuBX5d/XyRV0K+JDJjyxajTVUaFBTHZ9gngkTLviqTKeYTo+6U8fOt4YCWJ+hvgq8TbdiT1vt1En/8NdG6iPVVKhVU0dCfwReDmMn6HpMq5mejzO8sIKyhvSDjmIaI83FTy75GU1yairz9U5i8pLbCShP0ZcWjXaJkXIimbUaKP/wzKGQqOKbXCKhq+A/hv4JYyf5ekbG4h+viOMsMKyh8SjlkNfBR4tEu/T1J3PEr07dXd+GWlB1bLq8FW4YJSqVfsJPr0jF7ZNRNdqbCSp4argJ9343dKKt3PKYqQboQVdG9IOGY98BFm8dYMSZVwP9GXu3o6S9cCK0ngm4FP4WF/Ul0NEX34ZujOUHBMVyuslr2GX8NV8FLd7Cb6bil7BafS7d8HNBdkrQC+ApyXow2SZuRa4E3AwznCI2dgAZwKXAUcl6MdkqblbuBC4FbIEx7dnnSn5UJvBT4APJajHZLa9hjRV7OFFWQKrJYL/iHwX8SKeEnVs4Pooz+EfGEFGQMrufCx9VnfxEl4qWp2E32zq+ut9ib37wfGTcJ/EXhx7vZIavoJ8FYyTbK3qkIb0kn444gnh2fmbpMkbiSeCN4N1QiLKrQBGBdaZxGnFh6bu01SH7sHeCNwA1QnKLLOYaWSG3IDcCkderW1pGlbQ/TBSoUVVCiwYNyN+QnwQWBj7jZJfWYj0fd+AtUKK6hYYEHzBu0mlv5/FPh77jZJfeLvRJ+7EthdtbCCCgYWNENrmHiU+nFgW+42ST1uG9HXVgHDVQwrqGhgQTO0tgOfBT4NPJG7TVKPeoLoY58Ftlc1rKDCgQXN0BoCPgl8DlfDS522g+hbnwSGqhxWUPHAgmZobQWuAL5EDBUlzd4w0aeuALZWPawA5uZuQDsGgFHYDFxe/Ku3AAtyt0uqsR1EWF0ObK5DWEH1nlpOqlhcuh9wGfAOYGHuNkk19AQxDLyCGoUV1CywoBlai4H3AO8CFuVuk1Qj24gJ9k9Sk2Fgqm7tBZqhNQhcArwXeEruNkk18Hdi6cJnqcEE+0Tq2GagGVr7ABcD7wf2z90mqcI2EW+5WUXFly5Mpq7tBpqhNR+4CPgwcEjuNkkVtJY4LfRKKrwotB11bjvQDK0GcY7WfwLPyN0mqUL+BPw7sTewktttpqPu7QeedDTNp/A8LQniPKt3U8FTF2aqF64BeNIhgJ8AXkQNFsZKJdgN/JQ4IqYyh+91Qs906OQDuZs40vVrxF5EqZ9sJ/7uv5UeC6teu5amZIHpxcRarQNzt0nqgg3EGqtV1GxBaLt68ZqAZmjNAy4gniAen7tNUonuIp4EXg2M9GrH7tXrAp70humPAefSQ8NgiZiv+gXwPjK/5LQbevnagHGhtZzYg/gG3M6j3rAN+DqxJ3AN9H6H7vXrayqCaxFwIfH05MjcbZJm4QHiafhVwLZ+6cj9cp1AM7QGgNOJ7TznEvNcUl2MEEPAjwA3A6P91In76VqBcUPEg4C3E08SD8rdLqkNjxJPAD9f/HPfdeB+u96m5CniC4inK8/q5/uhShsFfk887f45PfwUcCr9et3AuGrrKOCdwOvw1AdVyybgm8BngPuhvzttP197U3JUzfnEhPxpwJzc7VJf2wXcQkysX0ONj4TpJO9BIam2DgPeBrwJWJq7XepL64GvAF8A/gp21DHehxbJ3NbZRLV1NnHmllS2YeB6oqq6nj6eq9ob78cEkmprKXE44JuBp+P9UjlGgT8DXyYO2VsP/mWbiPdkEsm6reOJV4u9EoeJ6qz1wHeJV27dRZ+tq5ou700biuBaQBwQ+A7gPOIlGNJMDQHXEq/bugHYYWecmveoTckwcV/iBIiLiU3Vzm9pOoaJTcqriJMVtoAdsV3ep2lq2Uz9cmIz9Um4xUeTGwFuJzYr/4A+2azcad6vGUrmtw4FXgG8HjgBmJu7baqUncCdwDeA7wN/w3mqGfO+zVISXIcTk/IXEm/uMbj6207ijTVXEZPqD2FQzZr3r0OS4DqSGCq+EjiRmKxX/9gB3EGE1A+IY2AMqg7xPnZYElzLgBcCrwbOABbnbptKtRW4Cfg28DNgHQZVx3k/S5JMzi8hVsu/BjgHOADve68YBR4HrgO+RaxO3wh+wGXxvpYsCa5B4JnAS4lN1kfjkoi6GgbuIzYl/wj4A7Guyg5VMu9vFxXhNRdYATyPWM91FvBU/CyqbhR4jFjkeTXwK+BhYKcfXPd4rzNIqq7FxMT8S4iq6xh8QUbVbAPuJaqpHxMT6lvBzpOD9zyzIrzmEHsUTwOeT8x5rcTtP7kMAauJOalfEudSrQd22WHy8v5XSDJkPJh4UcZYeB2B4VW2IeBB9oTUzcAjOOSrFD+LikrO5VpGnDf/bGJ5xLHEMc6eiDo7u4jjh+8hliP8jjg3fR2eQ1VZfi41kAwb9yPmuc4AziQ2Xx+C1Ve7hoC1xObjG4mguhfYjMO9WvAzqplkwn4hUX2dUnydROxlPJiYzG/kbmtmu4nJ8UeIvXy3A7cVX+uAJ8AOUDd+XjWXrKxfCBxIVGAnEwF2IrGEYjFRhfXq5z1KVE9biaUGdxAB9UeigtpABJQrz2vOz6/HJBXYfGIIuYx44riSWKy6ktjveAARYguoz9+DUWKv3hCxwvwB4mnefcX31UT1tJlY3FmbC1N7/Dz7RDIPtog4hPAw4GnEuV6HtHztT7z2bD4x8T+P8v+ujBJnRo0QYbOdmBRf2/K1BvgL8TaZLcQ6Keef+oSfc59LhpQLiIprkBhaHkqswF9CVGPp9yVE6C0gwmx+y/exwwzTAEq/7yDCZmPx9XjL98eIc6M2ENXUUPHfOKTrc/8PMsu1PGDpNu4AAAAldEVYdGRhdGU6Y3JlYXRlADIwMTEtMDYtMjdUMTM6MDc6MjktMDc6MDCHYldlAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDExLTA2LTI3VDEzOjA3OjI5LTA3OjAw9j/v2QAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII="""

REST_DURATION = 5
TOO_EARLY = 800
TOO_LATE = 1900
WORK_DURATION = 20


class PomodoroTimer(QtWidgets.QSystemTrayIcon):

    def __init__(self, work_icon_path, rest_icon_path, parent=None):
        super(PomodoroTimer, self).__init__()
        self.rest_icon = QtGui.QIcon(rest_icon_path)
        self.work_icon = QtGui.QIcon(work_icon_path)
        self.parent = parent

        self.cur_icon = self.work_icon
        self.setIcon(self.cur_icon)
        self.show()

        self.until = set_time(WORK_DURATION)

        menu = QtWidgets.QMenu(self.parent)
        menu.addAction('Exit')
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)
        self.display_msg_box()

    def display_msg_box(self):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Information)
        msgbox.setWindowIcon(self.cur_icon)
        if self.cur_icon == self.rest_icon:
            msgbox.setText('Rest until %s' % self.until)
        else:
            msgbox.setText('Work until %s' % self.until)
        msgbox.setFocus(True)
        msgbox.exec_()

    def exit(self):
        QtCore.QCoreApplication.exit()

    def update_icon(self):
        cur_time = int(time.strftime('%H%M'))
        if self.until <= cur_time:
            if self.cur_icon == self.rest_icon:
                self.cur_icon = self.work_icon
                self.until = set_time(WORK_DURATION)
            else:
                self.cur_icon = self.rest_icon
                self.until = set_time(REST_DURATION)
            self.setIcon(self.cur_icon)
            self.display_msg_box()


def find_already_running():
    if os.name == 'nt':
        # Ignore windows
        return
    run_count = 0
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        ps = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
        args = ps.split('\0')
        if len(args) > 2:
            if sys.argv[0] in args:
                run_count += 1
                if run_count > 1:
                    print '%s is already running' % sys.argv[0]
                    sys.exit()


def tray_icon(work_icon_path, rest_icon_path):
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    wdgt = QtWidgets.QWidget()
    trayIcon = PomodoroTimer(work_icon_path, rest_icon_path, parent=wdgt)
    qtimer = QtCore.QTimer()
    qtimer.timeout.connect(trayIcon.update_icon)
    qtimer.start(1000)
    trayIcon.show()
    sys.exit(app.exec_())


def set_time(offset=0):
    ret_time = int(time.strftime('%H%M')) + offset
    if ret_time % 100 / 60 > 0:
        ret_time = ret_time + 40
    return ret_time


if __name__ == '__main__':
    work_icon = tempfile.NamedTemporaryFile(delete=True)
    work_icon.write(base64.decodestring(WORK_IMAGE))
    work_icon.flush()
    rest_icon = tempfile.NamedTemporaryFile(delete=True)
    rest_icon.write(base64.decodestring(REST_IMAGE))
    rest_icon.flush()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # find_already_running()
    tray_icon(work_icon.name, rest_icon.name)
