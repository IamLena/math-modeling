import random


class Generator:
	def __init__(self, base, err):
		self.low = base - err
		self.high = base + err

	def generation_time(self):
		return random.randint(self.low, self.high)


class Master ():
	def __init__(self, bases, errs):
		self.ops = [Generator(bases[0], errs[0]),
					Generator(bases[1], errs[1]),
					Generator(bases[2], errs[2]),
					Generator(bases[3], errs[3]),
					Generator(bases[4], errs[4])]

class ClientGenerator():
	def __init__(self, bases, errs):
		self.clients = [Generator(bases[0], errs[0]),
					Generator(bases[1], errs[1]),
					Generator(bases[2], errs[2]),
					Generator(bases[3], errs[3]),
					Generator(bases[4], errs[4])]


class EventModel:
	def __init__(self):
		self.time = 0
		self.endtime = 420
		self.proc = [0, 0, 0, 0, 0]
		self.events = list()
		self.master = Master([20, 35,  55, 85, 105], [7, 10, 17, 25, 32])
		self.clients = ClientGenerator([13, 25, 38, 60, 73], [0, 0, 0, 0, 0])

	def newday(self):
		self.time = 0
		self.endtime = 420
		self.events = list()

	def print_info(self):
		print(self.time)
		print(self.endtime)
		print(self.days)
		print(self.proc)
		print(self.events)

	def generate_clients(self):
		for i in range (5):
			t = 0
			while t < self.endtime:
				t += self.clients.clients[i].generation_time()
				self._add_event([t, i])

	def modeling(self):
		self.generate_clients()
		i = 0
		while self.time < self.endtime and i < len(self.events):
			while self.time > self.events[i][0]:
				i += 1
			self.time = self.events[i][0]
			self.time += self.master.ops[self.events[i][1]].generation_time()
			if (self.time < self.endtime):
				self.proc[self.events[i][1]] += 1
			i += 1

	def get_result(self):
		summary = 0
		for i in self.proc:
			summary += i
		cost = 300 * self.proc[0] + \
				500 * self.proc[1] + \
				800 * self.proc[2] + \
				1300 * self.proc[3] + \
				1600 * self.proc[4]

		print ("op1: ", self.proc[0])
		print ("op2: ", self.proc[1])
		print ("op3: ", self.proc[2])
		print ("op4: ", self.proc[3])
		print ("op5: ", self.proc[4])
		print ("clients processed: ", summary)
		print ("cost: ", cost)


	def _add_event(self, event: list):
		i = 0
		while i < len(self.events) and self.events[i][0] < event[0]:
			i += 1
		self.events.insert(i, event)


if __name__ == "__main__":
	model = EventModel()
	model.modeling()
	model.newday()
	model.modeling()
	model.newday()
	model.modeling()
	model.get_result()
