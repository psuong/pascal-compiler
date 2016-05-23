program arrays;
    var a: array[0..10] of integer;
    var x: integer;
    var i: integer;
    var t: integer;
    var l: integer;
begin
    x := 10;

    for i:= 0 to 10 do
        begin
            a[i] := x * i;
            l := a[i];
            t := l div 2;
            writeln(t);
        end;
end.
