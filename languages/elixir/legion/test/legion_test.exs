defmodule LegionTest do
  use ExUnit.Case
  doctest Legion

  test "basic" do
    IO.inspect Legion.march("node()")
  end
end
