import numpy.random as rand
import math

def getPoisson(lambda_p):
	L = math.exp(-lambda_p)
	p = rand.uniform(0, 1)
	k = 1
	while (p > L):
		k += 1
		p *= rand.uniform(0, 1)
	return k - 1


def getUniform(a, b):
	return round(rand.uniform(a, b), 5)

def is_in(value, array):
	for i in range(len(array)):
		if (abs(value - array[i]) < 0.00000001):
			return i
	return -1

class Model:
	def __init__ (self, body):
		self.a = body.a
		self.b = body.b
		self.lambda_p = body.lambda_p
		self.request_quantity = body.request_quantity
		self.reentry_probability = body.reentry_probability
		self.delta_t = body.delta_t
		self.t0 = body.t0
		self.tn = body.tn
		self.maxqueuelength = 0
		self.requests = []
		self.services = []

		self.quantity_t = 0
		self.quantity_e = 0
		self.queue_t = 0
		self.queue_e = 0

	def generate_requests(self):
		for i in range(self.request_quantity):
			self.requests.append(float(getUniform(self.a, self.b)))
		(self.requests).sort()

	def generate_services(self):
		curt = getPoisson(self.lambda_p)
		while (curt < self.tn):
			self.services.append(int(curt))
			curt += getPoisson(self.lambda_p)

	def stepbystep(self):
		requests_copy = self.requests[:]
		curt = self.t0
		while (curt < self.tn):
			if (is_in(curt, requests_copy) != -1):
				self.queue_t += 1
			service_index = is_in(curt, self.services)
			if (service_index != -1):
				self.queue_t -= 1
				self.quantity_t += 1
				if (rand.uniform(0, 1) > self.reentry_probability):
					self.queue_t+= 1
					requests_copy.append(float(curt + getPoisson(self.lambda_p)))
					requests_copy.sort()
			curt += self.delta_t
		print(requests_copy)
		print(requests_copy[0])

	def event_modeling(self):
		requests_copy = self.requests[:]
		services_copy = self.services[:]
		print(requests_copy)
		print(services_copy)
		curt = self.t0
		while (curt < self.tn and len(requests_copy) > 0 and len(services_copy) > 0):
			if (requests_copy[0] <= services_copy[0]):
				self.queue_e += 1
				curt = requests_copy[0]
				requests_copy.pop(0)
			else: #(requests_copy[0] > services_copy[0])
				self.queue_e -= 1
				self.quantity_e += 1
				if (rand.uniform(0, 1) > self.reentry_probability):
					self.queue_e+= 1
					requests_copy.append(float(curt + getPoisson(self.lambda_p)))
					requests_copy.sort()
				curt = services_copy[0]
				services_copy.pop(0)

class Params:
	def __init__(self, a, b, lambda_p, request_quantity, reentry_probability, delta_t, t0, tn):
		self.a = a
		self.b = b
		self.lambda_p = lambda_p
		self.request_quantity = request_quantity
		self.reentry_probability = reentry_probability
		self.delta_t = delta_t
		self.t0 = t0
		self.tn = tn

pars = Params(0, 30, 3, 10, 0, 0.00001, 0, 30)

m = Model(pars)
m.generate_requests()
m.generate_services()
# m.stepbystep()
m.event_modeling()
print(m.queue_t, m.quantity_t)
print(m.queue_e, m.quantity_e)