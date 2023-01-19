from inspect import Parameter, Signature

fields = ['name', 'age', 'friends']
params = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in fields]
sig = Signature(params)

def func(*args, **kwargs):
    bound_args = sig.bind(*args, **kwargs)
    for name, val in bound_args.arguments.items():
        print(name, '=', val)


def main():
    func('Fred', 24, [])


if __name__ == '__main__':
    exit(main())
