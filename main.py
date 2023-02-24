# autopep8: off
# Must run line before using submodule
import sys
import os
sys.path.append(os.path.dirname(__file__) + "/ner_processing")

from nero_view import NeroView



if __name__ == "__main__":
    controller = NeroView()
    controller.run()
