# switch

## Description

This mini-app will, every 20 minutes, advice you to switch your current task to another one. It is a simple way to avoid getting stuck on a task and to keep your mind fresh.

I built this mini-app to apply interleaved practice to my daily work. Interleaved practice is a learning technique that consists of mixing different topics or tasks during a study session. This technique has been proven to be more effective than blocked practice, where you focus on a single topic or task for a long period of time.

It also, according to my hypothesis, helps to avoid procrastination by feeling less bored by being burnt out on a task.
## How to use

You need to have installed the following python 3 packages:

- `windows_toasts`

- `pystray`

- `pillow` or `PIL` for short.

You can install them by running:

```bash
pip install windows_toasts pystray pillow
```

Then, you can run the script by just executing the `switch.pyw` file.

Do notice that in fact, this is only a Windows app. If it's not clear by the use of `windows_toasts`.

## Exiting the app

To exit the app, you can right-click on the tray icon and select the `Exit` option. The icon is a blue circle on a white background.

## Interleaved practice

If you want to know more about interleaved practice, I recommend you read Justin Skycak's blog:

>During review, it's also best to spread minimal effective doses of practice across various skills. This is known as mixed practice or interleaving -- it's the opposite of "blocked" practice, which involves extensive consecutive repetition of a single skill. Blocked practice can give a false sense of mastery and fluency because it allows students to settle into a robotic rhythm of mindlessly applying one type of solution to one type of problem. Mixed practice, on the other hand, creates a "desirable difficulty" that promotes vastly superior retention and generalization, making it a more effective review strategy.

You can read the full article [here](https://www.justinmath.com/which-cognitive-psychology-findings-are-solid-that-can-be-used-to-help-students-learn-better).

## Future improvements

Will probably not do, but will leave as ideas regardless.

- Logging the tasks you are working on and the time you spent on them to analyze your productivity and find your least productive times.

- Adding a configuration file to change the time interval between switches.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License (MIT) is used because of it's rather permissive nature.