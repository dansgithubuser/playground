defmodule Legion do
  @moduledoc """
  Documentation for Legion.
  """

  use Application

  def start(_type, _args) do
    IO.puts "Hello, world!"
    Supervisor.start_link([], [strategy: :one_for_one])
  end
end
