defmodule Legion do
  @moduledoc """
  Documentation for Legion.
  """

  use Application

  def start(_type, _args) do
    case System.get_env("LEGION") do
      nil -> nil
      x -> Node.connect(String.to_atom("legion@" <> x))
    end
    import Supervisor.Spec
    Supervisor.start_link(
      [
        supervisor(Task.Supervisor, [[name: Legion.TaskSupervisor]])
      ],
      [
        strategy: :one_for_one
      ]
    )
  end

  def march(f) do
    nodes = Node.list ++ [Node.self]
    tasks = for {node, i} <- Enum.with_index(nodes) do Task.Supervisor.async(
      {Legion.TaskSupervisor, node},
      Legion,
      :march,
      [f, length(nodes), i]
    ) end
    for i <- tasks, do: Task.await(i)
  end

  def march(f, n, i) do
    Code.eval_string(f, [n: n, i: i])
  end
end
