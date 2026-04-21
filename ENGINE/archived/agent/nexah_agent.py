class NexahAgent:
    def __init__(self, config=None):
        self.config = config or {}
        self.state = {}

    def run(self):
        print("NEXAH Agent started")

        # 1. load model / setup
        self.initialize()

        # 2. execute main loop
        self.loop()

    def initialize(self):
        print("Initializing system...")
        # TODO: connect kernel / load modules

    def loop(self):
        print("Entering main loop...")
        for step in range(3):
            print(f"Step {step}")
            self.step()

    def step(self):
        # Beispiel: Kernel call
        result = self.kernel_call()

        # Interpretation / decision
        self.process(result)

    def kernel_call(self):
        print("Calling kernel...")
        # TODO: echte Kernel-Integration
        return {"status": "ok", "value": 42}

    def process(self, result):
        print(f"Processing result: {result}")
