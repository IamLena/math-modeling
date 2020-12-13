import random


class Generator:
	def __init__(self, base, err):
		self.low = base - err
		self.high = base + err

	def generation_time(self):
		return random.randint(self.low, self.high)


class Operator(Generator):
	def __init__(self, base, err):
		super().__init__(base, err)
		self.busy = False


class PC:
	def __init__(self, time):
		self.generation_time = time
		self.busy = False


class EventModel:
	def __init__(self, n):
		self.n = n
		self.events = list()
		self.clients = Generator(10, 2)
		self.operators = [Operator(20, 5), Operator(40, 10), Operator(40, 20)]
		self.pcs = [PC(15), PC(30)]
		self.lines = [0, 0]
		self.processed = 0
		self.lost = 0

	def reset(self, n):
		self.n = n
		self.events = list()
		self.clients = Generator(10, 2)
		self.operators = [Operator(20, 5), Operator(40, 10), Operator(40, 20)]
		self.pcs = [PC(15), PC(30)]
		self.lines = [0, 0]
		self.processed = 0
		self.lost = 0

	def modeling(self):
		self._add_event([self.clients.generation_time(), 'client'])
		while self.processed + self.lost < self.n:
			event = self.events.pop(0)
			if event[1] == 'client':
				self.new_client(event[0])
			elif event[1] == 'operator':
				self.operator_done(event)
			elif event[1] == 'pc':
				self.pc_done(event)
		return self.lost

	def new_client(self, time):
		i = 0
		while i < 3 and self.operators[i].busy:
			i += 1
		if i == 3:
			self.lost += 1
		else:
			self.operators[i].busy = True
			self._add_event([time + self.operators[i].generation_time(), 'operator', i])
		self._add_event([time + self.clients.generation_time(), 'client'])

	def operator_done(self, event):
		self.operators[event[2]].busy = False
		if event[2] < 2:
			self.lines[0] += 1
			event[2] = 0
		else:
			self.lines[1] += 1
			event[2] = 1
		self.pc_getjob(event)

	def pc_getjob(self, event):
		pcnum = event[2]
		if not self.pcs[pcnum].busy and self.lines[pcnum] > 0:
			self.pcs[pcnum].busy = True
			self._add_event([event[0] + self.pcs[pcnum].generation_time, 'pc', pcnum])
			self.lines[pcnum] -= 1

	def pc_done(self, event):
		self.pcs[event[2]].busy = False
		self.processed += 1
		self.pc_getjob(event)

	def _add_event(self, event: list):
		i = 0
		while i < len(self.events) and self.events[i][0] < event[0]:
			i += 1
		self.events.insert(i, event)


if __name__ == "__main__":
	n = 300
	model = EventModel(n)
	model.modeling()
	n0 = model.processed
	n1 = model.lost
	print("Processed:", n0, "\nLost:", n1, "\nLost percent:", 100 * n1 / (n0 + n1))

	print('\nAverage (100 times)')
	n0 = 0
	n1 = 0
	times = 100
	for i in range(times):
		model.reset(n)
		model.modeling()
		n0 += model.processed
		n1 += model.lost
	n0 /= times
	n1 /= times
	print("Processed:", n0, "\nLost:", n1, "\nLost percent:", 100 * n1 / (n0 + n1))
