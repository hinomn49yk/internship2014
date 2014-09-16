class HelloWorld
  def initialize(myname = "Ruby")
    @name = myname
  end

  def hello
    puts "Hello, world. I am #{@name}."
  end
  def goodbye
    puts "Good Bye! #{@name}."
  end
  attr_accessor :name
  
  def greet
    puts "Hi, I am #{self.name}"
  end


end

bob = HelloWorld.new("Bob")
ruby = HelloWorld.new
yoshiki = HelloWorld.new("Yoshiki")

p bob
p bob.name
bob.name = "Rob"
bob.hello #HelloWorldクラスのインスタンスであるBobにはhelloというインスタンスメソッドが用意されている。
bob.greet
ruby.hello
yoshiki.goodbye

# 以下はエラー
#sekine = "Sekine"
#sekine.hello # Stringクラスのインスタンスであるsekineにはhelloというインスタンスメソッドが定義されていない。NoMethod Errorとなる。
