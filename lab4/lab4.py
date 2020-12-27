import numpy.random as rand
import math
from prettytable import PrettyTable


decimals = 4

def getPoisson(lambda_p):
	L = math.exp(-lambda_p)
	p = rand.uniform(0, 1)
	k = 1
	while (p > L):
		k += 1
		p *= rand.uniform(0, 1)
	return k - 1


def getUniform(a, b):
	# return round(rand.uniform(a, b), decimals)
	return rand.uniform(a, b)

def is_in(value, array):
	for i in range(len(array)):
		if (array[i] >= 0 and abs(value - array[i]) < 0.00001):
			array[i] = -1
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
		self.maxqueuelength_t = 0
		self.maxqueuelength_e = 0
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

	def generate_services(self, curt):
		curt = math.ceil(float(curt))
		while (curt < self.tn):
			self.services.append(float(curt))
			curt += getPoisson(self.lambda_p)

	def generate_events(self):
		self.generate_requests()
		self.generate_services(self.requests[0])


	def stepbystep(self):
		requests_copy = self.requests[:]
		services_copy = self.services[:]
		curt = self.t0
		while (curt < self.tn):
			if (is_in(curt, requests_copy) != -1):
				self.queue_t += 1
				if (self.maxqueuelength_t < self.queue_t):
					self.maxqueuelength_t = self.queue_t
			service_index = is_in(curt, services_copy)
			if (service_index != -1):
				if (self.queue_t > 0):
					self.queue_t -= 1
					self.quantity_t += 1
					if (rand.uniform(0, 1) < self.reentry_probability):
						self.queue_t += 1
						requests_copy.append(float(curt + getPoisson(self.lambda_p)))
						requests_copy.sort()
			curt += self.delta_t

	def event_modeling(self):
		requests_copy = self.requests[:]
		services_copy = self.services[:]
		curt = self.t0
		while (curt < self.tn):
			if ((len(requests_copy) > 0 and len(services_copy) == 0) or (len(requests_copy) > 0) and (len(services_copy) > 0) and (requests_copy[0] <= services_copy[0])):
				self.queue_e += 1
				if (self.maxqueuelength_e < self.queue_e):
					self.maxqueuelength_e = self.queue_e
				curt = requests_copy[0]
				if (len(requests_copy) > 0 and len(services_copy) > 0 and requests_copy[0] == services_copy[0]):
					services_copy.pop(0)
				requests_copy.pop(0)
			elif ((len(services_copy) > 0 and len(requests_copy) == 0) or (len(requests_copy) > 0) and (len(services_copy) > 0) and (requests_copy[0] > services_copy[0])):
				if (self.queue_e > 0):
					self.queue_e -= 1
					self.quantity_e += 1
					if (rand.uniform(0, 1) < self.reentry_probability):
						self.queue_e += 1
						requests_copy.append(float(curt + getPoisson(self.lambda_p)))
						requests_copy.sort()
				curt = services_copy[0]
				services_copy.pop(0)
			else:
				break
	def print_result(self):
		tbl = PrettyTable()
		tbl.field_names = ["", "max queue length", "number of processed requests"]
		tbl.add_row(["delta_t", self.maxqueuelength_t, self.quantity_t])
		tbl.add_row(["events", self.maxqueuelength_e, self.quantity_e])
		print(tbl)

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
	def print_params(self):
		print("a:\t\t\t", self.a)
		print("b:\t\t\t", self.b)
		print("lambda:\t\t\t", self.lambda_p)
		print("number of requests:\t", self.request_quantity)
		print("reentry probability:\t", self.reentry_probability)
		print("start time:\t\t", self.t0)
		print("end time:\t\t", self.tn)
		print("time step:\t\t", self.delta_t)
		print()

pars = Params(0, 10, 5, 60, 0, 0.00001, 0, 30)

pars.print_params()
m = Model(pars)
m.generate_events()
print("moments of request comming: ")
print(m.requests)
print()
print("moments of process events: ")
print(m.services)
print()
m.stepbystep()
m.event_modeling()
m.print_result()
