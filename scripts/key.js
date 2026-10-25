// osascript -l JavaScript key.js <keycode> <seconds held>: a real key
// press, down and later up, posted as the hardware would.
ObjC.import("CoreGraphics");
ObjC.import("Foundation");
function run(argv) {
  var code = parseInt(argv[0]), hold = parseFloat(argv[1] || "0.1");
  $.CGEventPost($.kCGHIDEventTap, $.CGEventCreateKeyboardEvent($(), code, true));
  $.NSThread.sleepForTimeInterval(hold);
  $.CGEventPost($.kCGHIDEventTap, $.CGEventCreateKeyboardEvent($(), code, false));
}
