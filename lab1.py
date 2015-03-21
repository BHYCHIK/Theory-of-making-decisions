import math
from scipy.optimize import minimize

class JobOffer(object):
    salary_modifier = 50
    like_modifier = 0.04
    time_to_get_bad = 180

    middle_speed = 0.5 # meters in minute

    def __init__(self, x, y):
        distance = math.sqrt( x ** 2 + y ** 2)

        self._distance = distance

        self.salary = JobOffer.salary_modifier * distance
        self.like = JobOffer.like_modifier * distance * distance
        self.time_to_get = distance / JobOffer.middle_speed

        self._is_parking_resticted = (math.fabs(x) > 5) or (math.fabs(y) > 7)
        if self._is_parking_resticted:
            self.salary = self.salary * 1.4

    
    def count_good_factor(self):
        if self.time_to_get >= JobOffer.time_to_get_bad:
            return 0
        result = (math.sqrt(self.salary) + (self.like ** 2)) * (math.log(JobOffer.time_to_get_bad - self.time_to_get) ** 3)
        if self._is_parking_resticted:
            result = result / 4
        return result


    def __str__(self):
        return 'distance = %s) salary = %s, like = %s, time to get = %s parking = %s result = %s' % (self._distance, self.salary, self.like, self.time_to_get, not self._is_parking_resticted, self.count_good_factor())


x = minimize(lambda args: 1 / (JobOffer(args[0], args[1]).count_good_factor() + 0.0000001), [0.0, 0.0], method='nelder-mead', options={'xtol': 1e-8, 'disp': True}).x
print(x[0], x[1])
best_job = JobOffer(x[0], x[1])
print('Best job: %s', best_job)
