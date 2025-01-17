import java
import semmle.code.java.dataflow.TaintTracking
import TestUtilities.InlineExpectationsTest
private import semmle.code.java.dataflow.ExternalFlow

module Config implements DataFlow::ConfigSig {
  predicate isSource(DataFlow::Node n) {
    n.asExpr().(MethodAccess).getCallee().getName() = "source"
    or
    sourceNode(n, "kotlinMadFlowTest")
  }

  predicate isSink(DataFlow::Node n) {
    n.asExpr().(Argument).getCall().getCallee().getName() = "sink"
    or
    sinkNode(n, "kotlinMadFlowTest")
  }
}

module Flow = TaintTracking::Global<Config>;

class InlineFlowTest extends InlineExpectationsTest {
  InlineFlowTest() { this = "HasFlowTest" }

  override string getARelevantTag() { result = "flow" }

  override predicate hasActualResult(Location location, string element, string tag, string value) {
    tag = "flow" and
    exists(DataFlow::Node sink | Flow::flowTo(sink) |
      sink.getLocation() = location and
      element = sink.toString() and
      value = ""
    )
  }
}
