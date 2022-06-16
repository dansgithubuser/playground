use std::time::{Duration, Instant};

//===== state =====//
enum State {
    Idle,
    Ticking { last_tick: Instant },
}

struct Stopwatch {
    duration: Duration,
    state: State,
    toggle: iced::button::State,
    reset: iced::button::State,
}

//===== messages =====//
#[derive(Debug, Clone)]
enum Message {
    Toggle,
    Reset,
    Tick(Instant),
}

//===== app =====//
impl iced::Application for Stopwatch {
    type Executor = iced::executor::Default;
    type Message = Message;
    type Flags = ();

    fn new(_: Self::Flags) -> (Stopwatch, iced::Command<Message>) {
        (
            Stopwatch {
                duration: Duration::default(),
                state: State::Idle,
                toggle: iced::button::State::new(),
                reset: iced::button::State::new(),
            },
            iced::Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("Stopwatch")
    }

    fn update(&mut self, message: Message) -> iced::Command<Message> {
        match message {
            Message::Toggle => match self.state {
                State::Idle => {
                    self.state = State::Ticking {
                        last_tick: Instant::now(),
                    };
                }
                State::Ticking { .. } => {
                    self.state = State::Idle;
                }
            },
            Message::Tick(now) => match &mut self.state {
                State::Ticking { last_tick } => {
                    self.duration += now - *last_tick;
                    *last_tick = now;
                }
                _ => (),
            },
            Message::Reset => {
                self.duration = Duration::default();
            },
        }

        iced::Command::none()
    }

    fn subscription(&self) -> iced::Subscription<Message> {
        match self.state {
            State::Idle => iced::Subscription::none(),
            State::Ticking { .. } => {
                iced::time::every(Duration::from_millis(10)).map(Message::Tick)
            }
        }
    }

    fn view(&mut self) -> iced::Element<Message> {
        let seconds = self.duration.as_secs();

        let duration = iced::Text::new(format!(
            "{:0>2}:{:0>2}:{:0>2}.{:0>2}",
            seconds / 60,
            (seconds % 60) / 60,
            seconds % 60,
            self.duration.subsec_millis() / 10,
        ))
        .size(40);

        let button = |state, label| {
            iced::Button::new(
                state,
                iced::Text::new(label)
                    .horizontal_alignment(iced::alignment::Horizontal::Center),
            )
            .padding(10)
            .width(iced::Length::Units(80))
        };

        let toggle_button = {
            let label = match self.state {
                State::Idle => "Start",
                State::Ticking { .. } => "Stop",
            };

            button(&mut self.toggle, label).on_press(Message::Toggle)
        };

        let reset_button =
            button(&mut self.reset, "Reset")
                .on_press(Message::Reset);

        let controls = iced::Row::new()
            .spacing(20)
            .push(toggle_button)
            .push(reset_button);

        let content = iced::Column::new()
            .align_items(iced::Alignment::Center)
            .spacing(20)
            .push(duration)
            .push(controls);

        iced::Container::new(content)
            .width(iced::Length::Fill)
            .height(iced::Length::Fill)
            .center_x()
            .center_y()
            .into()
    }
}

pub fn main() -> iced::Result {
    use iced::Application;
    Stopwatch::run(iced::Settings::default())
}
