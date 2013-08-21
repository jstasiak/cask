from nose.tools import eq_, raises

from cask import Cask


@raises(Exception)
def test_app_without_target_fails_to_run():
    app = Cask()
    app.run()


def test_execution_order_is_generally_correct():
    app = Cask()
    history = []

    @app.module
    def configure(binder):
        history.append('injection configuration')

    @app.before_main
    def before():
        history.append('before main')

    @app.after_main
    def after(result):
        history.append('after main, result: %s' % (result,))
        raise Exception('xxx')

    @app.exception_handler(Exception)
    def handle_exception(e):
        history.append('Unhandled exception: %s' % (e,))

    @app.main
    def main():
        history.append('main')
        return 123

    app.run()

    eq_(history,
        ['injection configuration', 'before main', 'main',
         'after main, result: 123', 'Unhandled exception: xxx'])
